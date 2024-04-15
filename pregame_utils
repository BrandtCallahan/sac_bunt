import pandas as pd

from mlb_stats import stats


def get_lineup(season_years: list, team_lineup: list):
    """
    season_years: list of years used to gather player/team stats
    team_lineup: list of players in the batting lineup

    :return:
        list
        [['tm', 'player1', PA, OBP, SLG, 1B, 2B, 3B, HR, GO, FO, SO, BB], ..., [Opp Fld%]]
    """
    # lineup creation
    team = str(input(f"What team is up to bat?\n")).upper()
    opp = str(input(f"Who is {team}'s opponent?\n")).upper()

    # matchup
    stats_df = stats(season_years)
    batting_df = stats_df[0]
    fielding_df = stats_df[2]

    # setting up lineup and pitching rotation
    # team_lineup = []
    # for player in range(1, 10):
    #     team_lineup += [input(f"Enter #{player} batter's name: \n")]

    lineup = pd.DataFrame()
    lineup_stats = []
    for n, player in enumerate(team_lineup):
        temp = batting_df[(batting_df["Name"].str.lower() == player.lower())][
            [
                "Name",
                "OBP",
                "SLG",
                "PA",
                "H",
                "1B",
                "2B",
                "3B",
                "HR",
                "GO",
                "FO",
                "SO",
                "BB",
            ]
        ]
        lineup = pd.concat([lineup, temp]).reset_index(drop=True)

        lineup_stats += [
            [
                team,
                lineup["Name"][n],
                lineup["OBP"][n],
                lineup["SLG"][n],
                lineup["PA"][n],
                lineup["H"][n],
                lineup["1B"][n],
                lineup["2B"][n],
                lineup["3B"][n],
                lineup["HR"][n],
                lineup["GO"][n],
                lineup["FO"][n],
                lineup["SO"][n],
                lineup["BB"][n],
            ]
        ]

    lineup_stats += [
        float(fielding_df[fielding_df["Tm"] == opp]["Fld%"].reset_index(drop=True)[0])
    ]
    lineup_stats += [team, opp]

    return lineup_stats
