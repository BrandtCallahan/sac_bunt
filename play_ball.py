import datetime

from inning_utils import *


def sac_bunt(n, season_years=None, tm_lineup=None):
    """
    n: int
        number of times to run inning simulation
    season_years:
        season years to use in stat gathering
    tm_lineup:
        team batting lineup

    :return:
        df
        columns = [player name, run% w/ bunt, total runs w/ bunt, run% w/o bunt, total runs w/o bunt, run% differential with respect to bunting]
    """

    if season_years is None:
        season_years = [2023]

    if tm_lineup is None:
        # Default: ATL Brave '23 Opening Day lineup
        tm_lineup = [
            "Ronald Acuna",
            "Ozzie Albies",
            "Austin Riley",
            "Matt Olson",
            "Marcell Ozuna",
            "Michael Harris",
            "Sean Murphy",
            "Orlando Arcia",
            "Jarred Kelenic",
        ]

    # lineup stats
    if season_years is None:
        if datetime.datetime.now().month < 6:
            season_years = [datetime.datetime.now().year - 1]
        else:
            season_years = [datetime.datetime.now().year]
    tm_stats = Lineup(season_years, tm_lineup)
    bat_lineup = tm_stats[0:9]
    opp_field = tm_stats[-3]
    matchup = f"{tm_stats[-2]} vs. {tm_stats[-1]}"

    tm_df = pd.DataFrame()

    # run through every batter (tracking the results)
    for batter in range(9):

        # tracking runs scored in the innings starting with the respective hitters
        bunt_run = 0
        bunt_r_total = 0
        swing_run = 0
        swing_r_total = 0

        # for each batter simulate n number of times
        for i in range(n):
            # sac bunt
            bunt = inning(
                bat_lineup,
                opp_field,
                batter=batter,
                o=1,
                aPOSlist=[0, 1, 0],
            )
            bunt_rt = bunt[0]
            bunt_r_total += bunt_rt
            if bunt_rt > 0:
                bunt_run += 1
            else:
                bunt_run += 0

            # swing away
            swing_away = inning(
                bat_lineup,
                opp_field,
                batter=batter,
                o=0,
                aPOSlist=[1, 0, 0],
            )
            swing_rt = swing_away[0]
            swing_r_total += swing_rt
            if swing_rt > 0:
                swing_run += 1
            else:
                swing_run += 0

        # create player df with results
        player_df = pd.DataFrame(
            data={
                "player_nm": [bat_lineup[batter][1]],
                "bunt_r%": [bunt_run / n],
                "bunt_r_total": [bunt_r_total],
                "swing_r%": [swing_run / n],
                "swing_r_total": [swing_r_total],
            }
        )
        player_df["r%_diff"] = player_df["bunt_r%"] - player_df["swing_r%"]

        # compile all players into tm df
        tm_df = pd.concat([tm_df, player_df]).reset_index(drop=True)

    return tm_df
