from requests import get
from pprint import PrettyPrinter

BASE_URL = "https://data.nba.net"
TO_DAY_DATA = "/prod/v1/today.json"

printer = PrettyPrinter()


def get_links():
    nbaData = get(BASE_URL + TO_DAY_DATA).json()
    return nbaData['links']


def get_scoreboard():
    currentScoreboard = get_links()['currentScoreboard']
    games = get(BASE_URL + currentScoreboard).json()['games']
    print(get_links())

    for game in games:
        home_team = game['hTeam']
        away_team = game['vTeam']
        clock = game['clock']
        period = game['period']

        print("-------------------------------------------------------")
        print(
            f"{home_team['triCode']} vs {away_team['triCode']}")

        print(f"{home_team['score']} - {away_team['score']}")
        print(f"{clock} - {period['current']}")


def get_league_team_stats():
    stats = get_links()["leagueTeamStatsLeaders"]

    teams_preseason = get(
        BASE_URL + stats).json()["league"]['standard']["preseason"]["teams"]

    teams = list(filter(lambda x: x["name"] != "Team", teams_preseason))
    teams.sort(key=lambda x: int(x["ppg"]["rank"]))

    for i, team in enumerate(teams):
        name = team['name']
        nickname = team["nickname"]
        ppg = team['ppg']["avg"]
        print(f"{i + 1 }. {name} - {nickname} - {ppg}")


get_league_team_stats()
