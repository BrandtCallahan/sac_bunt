from random import uniform

import pandas as pd

from inning_utils import baserunning, AtBat
from pregame_utils import get_lineup


# run through the lineup
def Lineup(
    season_years,
    team_lineup,
):
    """
    :param season_years:
    :param team_lineup:

    :return:
        list
        [['tm', 'player1', OBP, SLG, 1B, 2B, 3B, HR], ..., [Opp Fld%]]
    """
    game = get_lineup(season_years, team_lineup)
    matchup = [game[-2], game[-1]]
    lineup = game[0:9]
    team = matchup[0]
    opp = matchup[1]

    return game


def AtBat(obp, h, so, go, fo, fe):
    # this function lays out the groundwork for an atbat to take place
    """
    obp: On Base Percentage
    h: Hit Percentage ( (H/PA) / OBP )
        determines a hit vs. a walk
    so: Strike Out Percentage
    go: Ground Out Percentage
    fo: Fly Out Percentage
    fe: Opponent Team Fielding Percentage

    :return: list
        [strikeout, groundout, flyout, walk, hit, e, o]

    """
    out = 0
    ob = 0
    strikeout = 0
    groundout = 0
    flyout = 0
    walk = 0
    hit = 0
    e = 0
    o = pd.NA

    outcome = uniform(0, 1)  # hit/out
    error = uniform(0, 1)  # error/no error

    if outcome > obp:
        out = 1
        ob = 0
        e = 0
    if outcome <= obp:
        if error < fe:
            out = 0
            ob = 1
            e = 0
        else:
            out = 0
            ob = 0
            e = 1

    aboutcome = [out, ob, e]

    if aboutcome[0] == 1:
        outtype = uniform(0, 1)
        if outtype >= 0 and outtype <= go:
            groundout = 1
            out = 1
            # where did you ground out to
            go_dict = {
                "ss": 0.30,  # 0.30
                "3b": 0.55,  # 0.25
                "2b": 0.80,  # 0.25
                "1b": 0.95,  # 0.15
                "p": 1.00,  # 0.05
            }
            go_pos = uniform(0, 1)
            if go_pos <= go_dict["ss"]:
                o = "ss"
            elif go_pos > go_dict["ss"] and go_pos <= go_dict["3b"]:
                o = "3b"
            elif go_pos > go_dict["3b"] and go_pos <= go_dict["2b"]:
                o = "2b"
            elif go_pos > go_dict["2b"] and go_pos <= go_dict["1b"]:
                o = "1b"
            elif go_pos > go_dict["1b"] and go_pos <= go_dict["p"]:
                o = "p"
        elif outtype > go and outtype <= (go + fo):
            flyout = 1
            out = 1
            # where did you fly out to
            fo_dict = {
                "lf": 0.20,  # 0.20
                "cf": 0.40,  # 0.20
                "rf": 0.60,  # 0.20
                "ss": 0.75,  # 0.15
                "3b": 0.85,  # 0.10
                "2b": 0.80,  # 0.08
                "1b": 0.98,  # 0.05
                "c": 1.00,  # 0.02
            }
            fo_pos = uniform(0, 1)
            if fo_pos <= fo_dict["lf"]:
                o = "lf"
            elif fo_pos > fo_dict["lf"] and fo_pos <= fo_dict["cf"]:
                o = "cf"
            elif fo_pos > fo_dict["cf"] and fo_pos <= fo_dict["rf"]:
                o = "rf"
            elif fo_pos > fo_dict["rf"] and fo_pos <= fo_dict["ss"]:
                o = "ss"
            elif fo_pos > fo_dict["ss"] and fo_pos <= fo_dict["3b"]:
                o = "3b"
            elif fo_pos > fo_dict["3b"] and fo_pos <= fo_dict["2b"]:
                o = "2b"
            elif fo_pos > fo_dict["2b"] and fo_pos <= fo_dict["1b"]:
                o = "1b"
            elif fo_pos > fo_dict["1b"] and fo_pos <= fo_dict["c"]:
                o = "c"
        elif outtype >= (go + fo):
            strikeout = 1
            out = 1
            o = "p"
    elif aboutcome[1] == 1:
        obtype = uniform(0, 1)
        if obtype <= h:
            hit = 1
            ob = 1
        else:
            walk = 1
            ob = 1

    ab = [strikeout, groundout, flyout, walk, hit, e, o]

    return ab


# this lays the groundwork for baserunners moving around the bases
# it is atbat specific
def baserunning(
    bat_lineup,
    aPOSlist,
    atbat,
    batter,
):
    single = bat_lineup[batter][6]
    double = bat_lineup[batter][7] + single
    triple = bat_lineup[batter][8] + double
    homer = bat_lineup[batter][9] + triple

    basesruns = []
    SLG = atbat[2]

    if aPOSlist == [0, 0, 0]:
        if atbat[0] == 1:
            POSlist = [1, 0, 0]
            rs = 0
        elif atbat[1] == 1:
            if SLG <= single:  # nobody on and a single/walk
                POSlist = [1, 0, 0]
                rs = 0
            elif SLG <= double and SLG > single:  # nobody on and a double
                POSlist = [0, 1, 0]
                rs = 0
            elif SLG <= triple and SLG > double:  # nobody on and a triple
                POSlist = [0, 0, 1]
                rs = 0
            elif SLG <= homer and SLG > triple:  # nobody on and a homerun
                POSlist = [0, 0, 0]
                rs = 1

    elif aPOSlist == [1, 0, 0]:
        if atbat[0] == 1:
            POSlist = [1, 1, 0]
            rs = 0
        elif atbat[1] == 1:
            if SLG <= single:  # man on first and single/walk
                POSlist = [1, 1, 0]
                rs = 0
            elif SLG <= double and SLG > single:  # man on first and double
                POSlist = [0, 1, 1]
                rs = 0
            elif SLG <= triple and SLG > double:  # man on first and triple
                POSlist = [0, 0, 1]
                rs = 1
            elif SLG <= homer and SLG > triple:  # man on first and homerun
                POSlist = [0, 0, 0]
                rs = 2

    elif aPOSlist == [1, 1, 0]:
        if atbat[0] == 1:  # man on first and second and walk
            POSlist = [1, 1, 1]
            rs = 0
        elif atbat[1] == 1:
            if SLG <= single:  # man on first and second and single
                POSlist = [1, 1, 0]
                rs = 1
            elif SLG <= double and SLG > single:  # man on first and second and double
                POSlist = [0, 1, 1]
                rs = 1
            elif SLG <= triple and SLG > double:  # man on first and second and triple
                POSlist = [0, 0, 1]
                rs = 2
            elif SLG <= homer and SLG > triple:  # man on first and second and homerun
                POSlist = [0, 0, 0]
                rs = 3

    elif aPOSlist == [1, 0, 1]:
        if atbat[0] == 1:  # man on first and third and walk
            POSlist = [1, 1, 1]
            rs = 0
        elif atbat[1] == 1:
            if SLG <= single:  # man on first and third and single
                POSlist = [1, 1, 0]
                rs = 1
            elif SLG <= double and SLG > single:  # man on first and third and double
                POSlist = [0, 1, 1]
                rs = 1
            elif SLG <= triple and SLG > double:  # man on first and third and triple
                POSlist = [0, 0, 1]
                rs = 2
            elif SLG <= homer and SLG > triple:  # man on first and third and homerun
                POSlist = [0, 0, 0]
                rs = 3

    elif aPOSlist == [0, 1, 0]:
        if atbat[0] == 1:  # man on second and walk
            POSlist = [1, 1, 0]
            rs = 0
        elif atbat[1] == 1:
            if SLG <= single:  # man on second and single
                POSlist = [1, 0, 1]
                rs = 0
            elif SLG <= double and SLG > single:  # man on second and double
                POSlist = [0, 1, 0]
                rs = 1
            elif SLG <= triple and SLG > double:  # man on second and triple
                POSlist = [0, 0, 1]
                rs = 2
            elif SLG <= homer and SLG > triple:  # man on second and homerun
                POSlist = [0, 0, 0]
                rs = 3

    elif aPOSlist == [0, 1, 1]:
        if atbat[0] == 1:  # man on second and third and walk
            POSlist = [1, 1, 1]
            rs = 0
        elif atbat[1] == 1:
            if SLG <= single:  # man on second and third and single
                POSlist = [1, 0, 1]
                rs = 1
            elif SLG <= double and SLG > single:  # man on second and third and double
                POSlist = [0, 1, 0]
                rs = 2
            elif SLG <= triple and SLG > double:  # man on second and third and triple
                POSlist = [0, 0, 1]
                rs = 2
            elif SLG <= homer and SLG > triple:  # man on second and third and homerun
                POSlist = [0, 0, 0]
                rs = 3

    if aPOSlist == [0, 0, 1]:
        if atbat[0] == 1:  # man on third and walk
            POSlist = [1, 0, 1]
            rs = 0
        elif atbat[1] == 1:
            if SLG <= single:  # man on third and single
                POSlist = [1, 0, 0]
                rs = 1
            elif SLG <= double and SLG > single:  # man on third and double
                POSlist = [0, 1, 0]
                rs = 1
            elif SLG <= triple and SLG > double:  # man on third and triple
                POSlist = [0, 0, 1]
                rs = 1
            elif SLG <= homer and SLG > triple:  # man on third and homerun
                POSlist = [0, 0, 0]
                rs = 2

    if aPOSlist == [1, 1, 1]:
        if atbat[0] == 1:  # bases loaded and walk
            POSlist = [1, 1, 1]
            rs = 1
        elif atbat[1] == 1:
            if SLG <= single:  # bases loaded and single
                POSlist = [1, 1, 0]
                rs = 2
            elif SLG <= double and SLG > single:  # bases loaded and double
                POSlist = [0, 1, 1]
                rs = 2
            elif SLG <= triple and SLG > double:  # bases loaded and triple
                POSlist = [0, 0, 1]
                rs = 3
            elif SLG <= homer and SLG > triple:  # bases loaded and homerun
                POSlist = [0, 0, 0]
                rs = 4

    basesruns = [POSlist, rs]

    return basesruns


"""
aPOSlist = [1, 0, 0]  # man on first
aPOSlist = [0, 1, 0]  # man on second (after sac bunt)
"""


# now we set the groundwork for an inning to take place
def inning(
    bat_lineup=None,
    opp_field=None,
    batter=None,
    o=None,
    aPOSlist=None,
):
    """
    Default with a man on first: aPOSlist = [1, 0, 0]
    Other scenario will be man on second: aPOSlist = [0, 1, 0]

    bat_lineup: list
        lineup stats per batter
    opp_field: float
        opponent fielding pct. (FLD %)
    batter: int
        batter depicted by their number in the lineup (i.e. 0 == 1st batter in lineup)
    o: int
        outs in the inning (0 if no sac bunt, 1 if sac bunt)
    aPOSlist: list
        [1, 0, 0] == man on first

    :return: list
        totals of outcomes and runs scored
    """

    if o is None:
        o = 0  # Default: outs start at 0

    if aPOSlist is None:
        aPOSlist = [1, 0, 0]
    POSLIST = []  # list of runners moving around bases

    ht = 0  # hit total
    rt = 0  # run total
    rs = 0  # run scored
    rlist = []  # list of runs and when/how scored
    LOB = 0  # men left on base

    walkt = 0  # walk total
    singlet = 0  # single total
    doublet = 0  # double total
    triplet = 0  # triple total
    homerunt = 0  # homerun total

    strikeoutt = 0  # strikeout total
    groundoutt = 0  # groundout total
    flyoutt = 0  # flyout total

    pitchcount = 0
    atbatlist = []  # list the atbat outcomes in order

    if batter is None:
        batter = 0

    while o < 3:  # inning continues as long as there are less than 3 outs

        # player SLG %
        single = bat_lineup[batter][6]
        double = bat_lineup[batter][7] + single
        triple = bat_lineup[batter][8] + double
        homer = bat_lineup[batter][9] + triple

        AB = AtBat(
            bat_lineup[batter][2],
            ((bat_lineup[batter][5] / bat_lineup[batter][4]) / bat_lineup[batter][2]),
            bat_lineup[batter][10],
            bat_lineup[batter][11],
            bat_lineup[batter][12],
            opp_field,
        )

        # at bat: strikeout,groundout,flyout,walk,hit,pitchcount, batter num

        abSLG = uniform(0, 1)  # create the SLG % value

        atbat = [
            AB[3],  # walk
            AB[4],  # hit
            abSLG,
        ]  # pairs up the OBP (hit/no hit) and SLG (hit type)
        abWALK = atbat[0]
        abHIT = atbat[1]
        SLG = atbat[2]

        if abWALK == 1:
            y = 0
            h = 0  # walk(BB)/HBP
            walkt += 1
            atbatlist += ["walk"]
            # aPOSlist=[1,0,0]
        elif abHIT == 1:
            if SLG <= single:  # single liklihood
                y = 0
                h = 1  # single
                singlet += 1
                atbatlist += ["single"]
                # aPOSlist=[1,0,0]
            elif (SLG > single) or (SLG <= double):  # double liklihood
                y = 0
                h = 1  # double
                doublet += 1
                atbatlist += ["double"]
                # aPOSlist=[0,1,0]
            elif (SLG > double) or (SLG <= triple):  # triple liklihood
                y = 0
                h = 1  # triple
                triplet += 1
                atbatlist += ["triple"]
                # aPOSlist=[0,0,1]
            elif (SLG > triple) or (SLG <= homer):  # homerun liklihood
                y = 0
                h = 1
                atbatlist += ["homerun"]
                # aPOSlist=[0,0,0]
                homerunt += 1
        elif abWALK == 0 and abHIT == 0:  # obp is set up outside of the loop
            h = 0  # since out, no hit
            y = 1
            if AB[0] == 1:
                y = 1  # add an out
                strikeoutt += 1
                atbatlist += ["strikeout"]
                if POSLIST == []:
                    aPOSlist = [0, 0, 0]
                    rs = 0
                else:
                    aPOSlist = POSLIST[-1]  # return the previous baserunner list
                    rs = 0
            elif AB[1] == 1:
                y = 1  # add an out
                groundoutt = groundoutt + 1
                atbatlist = atbatlist + ["groundout"]
                if POSLIST == []:
                    aPOSlist = [0, 0, 0]
                    rs = 0
                else:
                    aPOSlist = POSLIST[-1]  # return the previous baserunner list
                    rs = 0
            elif AB[2] == 1:
                y = 1  # add an out
                flyoutt = flyoutt + 1
                atbatlist = atbatlist + ["flyout"]
                if POSLIST == []:
                    aPOSlist = [0, 0, 0]
                    rs = 0
                else:
                    aPOSlist = POSLIST[-1]  # return the previous baserunner list
                    rs = 0

        if abWALK == 1 or abHIT == 1:
            baserun = baserunning(bat_lineup, aPOSlist, atbat, batter)
            aPOSlist = baserun[
                0
            ]  # index out where players are on base shown in list form (i.e. [1,0,0] = man on first)
            rs = baserun[1]  # index out the runs scored

        POSLIST = POSLIST + [
            aPOSlist
        ]  # creates a list to keep track of where runners are on base after each new atbat

        rlist = rlist + [rs]  # list of runs scoring
        LOB = sum(POSLIST[-1])
        rt = rt + rs  # run total
        ht = ht + h  # hit total
        o = o + y  # out total

        if batter < 8:
            batter = batter + 1
        elif batter == 8:
            batter = 0

    off = [
        rt,
        ht,
        walkt,
        singlet,
        doublet,
        triplet,
        homerunt,
        LOB,
        strikeoutt,
        groundoutt,
        flyoutt,
        pitchcount,
        batter,
    ]

    return off
