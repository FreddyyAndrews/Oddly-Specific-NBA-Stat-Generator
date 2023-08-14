from datetime import datetime
import math
import os
from flask import Flask, jsonify
import requests
import random
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
CORS(
    app,
    resources={
        r"/*": {"origins": "https://oddly-specific-nba-stat-generator.netlify.app/"}
    },
)
base_url = os.getenv("supabase_base_url")
api_key = os.getenv("supabase_api_key")

int_to_season = {
    0: "1997-98",
    1: "1998-99",
    2: "1999-00",
    3: "2000-01",
    4: "2001-02",
    5: "2002-03",
    6: "2003-04",
    7: "2004-05",
    8: "2005-06",
    9: "2006-07",
    10: "2007-08",
    11: "2008-09",
    12: "2009-10",
    13: "2010-11",
    14: "2011-12",
    15: "2012-13",
    16: "2013-14",
    17: "2014-15",
    18: "2015-16",
    19: "2016-17",
    20: "2017-18",
    21: "2018-19",
    22: "2019-20",
    23: "2020-21",
    24: "2021-22",
}


def get_random_stat_line(caller: str) -> dict:
    """
    Retrieves a random stat line that matches the specified criteria.

    Args:
        caller (str): Identifier for the type of stat line required.
                      Accepts 'PRA', 'ALL', or 'EF'.

    Returns:
        dict: Randomly selected stat line that matches the criteria.

    Raises:
        ValueError: If no record could be found.
    """
    headers = {
        "apikey": api_key,
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    endpoint = ""
    if caller == "PRA":
        endpoint = "/rest/v1/Game Logs?PTS=gte.40&AST=gte.3&REB=gte.3&GAME_DATE_EST=gte.2010-01-01"

    if caller == "ALL":
        endpoint = "/rest/v1/Game Logs?PTS=gte.35&AST=gte.3&REB=gte.3&BLK=gte.2&STL=gte.2&GAME_DATE_EST=gte.2010-01-01"

    if caller == "EF":
        endpoint = "/rest/v1/Game Logs?PTS=gte.20&AST=gte.2&REB=gte.2&BLK=gte.2&STL=gte.2&FG_PCT=gte.0.5&GAME_DATE_EST=gte.2010-01-01"

    response = requests.get(
        f"{base_url}{endpoint}",
        headers=headers,
    )

    if response.json():
        response_dict = response.json()
        return response_dict[random.randint(0, len(response_dict) - 1)]
    else:
        raise ValueError("Could not find a record.")


def get_random_season_statline() -> dict:
    headers = {
        "apikey": api_key,
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    response = requests.get(
        f"{base_url}/rest/v1/Player Stats?PTS=gte.20&AST=gte.1&TRB=gte.2&SeasonInt=gte.10&G=gte.41&PTS=lt.30&AST=lt.6&TRB=lt.8",
        headers=headers,
    )

    if response.json():
        response_dict = response.json()
        return response_dict[random.randint(0, len(response_dict) - 1)]
    else:
        raise ValueError("Could not find a record.")


def get_better_season_statlines(statline: dict) -> list:
    headers = {
        "apikey": api_key,
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    points = statline["PTS"]
    rebounds = statline["TRB"]
    assists = statline["AST"]
    season = statline["SeasonInt"]

    response = requests.get(
        f"{base_url}/rest/v1/Player Stats?SeasonInt=lte.{season}&PTS=gte.{points}&TRB=gte.{rebounds}&AST=gte.{assists}&order=SeasonInt.desc",
        headers=headers,
    )

    return response.json()


def get_better_statlines(statline: dict, caller: str) -> list:
    """
    Retrieves a list of stat lines that are 'better' than a provided stat line.

    Args:
        statline (dict): Stat line to compare against.
        caller (str): Identifier for the type of stat line required.
                      Accepts 'PRA', 'ALL', or 'EF'.

    Returns:
        dict: List of stat lines that are 'better' than the input stat line.
    """
    headers = {
        "apikey": api_key,
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    points = statline["PTS"]
    rebounds = statline["REB"]
    assists = statline["AST"]
    date = statline["GAME_DATE_EST"]

    if caller == "ALL":
        blocks = statline["BLK"]
        steals = statline["STL"]

        response = requests.get(
            f"{base_url}/rest/v1/Game Logs?GAME_DATE_EST=lt.{date}&STL=gte.{steals}&BLK=gte.{blocks}&PTS=gte.{points}&REB=gte.{rebounds}&AST=gte.{assists}&order=GAME_DATE_EST.desc",
            headers=headers,
        )

    if caller == "PRA":
        response = requests.get(
            f"{base_url}/rest/v1/Game Logs?GAME_DATE_EST=lt.{date}&PTS=gte.{points}&REB=gte.{rebounds}&AST=gte.{assists}&order=GAME_DATE_EST.desc",
            headers=headers,
        )

    if caller == "EF":
        blocks = statline["BLK"]
        steals = statline["STL"]
        pct = statline["FG_PCT"]
        response = requests.get(
            f"{base_url}/rest/v1/Game Logs?GAME_DATE_EST=lt.{date}&FG_PCT=gt.{pct}&STL=gte.{steals}&BLK=gte.{blocks}&PTS=gte.{points}&REB=gte.{rebounds}&AST=gte.{assists}&order=GAME_DATE_EST.desc",
            headers=headers,
        )

    return response.json()


def add_suffix(n) -> str:
    """Add a suffix to an integer."""
    suffixes = {1: "st", 2: "nd", 3: "rd"}

    if 10 <= n <= 20:
        return "th"

    return suffixes.get(n % 10, "th")


def convert_date(date_str):
    date_object = datetime.strptime(date_str, "%Y-%m-%d")
    suffix = add_suffix(date_object.day)
    return date_object.strftime(f"%B {date_object.day}{suffix}, %Y")


def get_random_date_comparison(better_statlines: list) -> list:
    """
    Gets a random comparator value from a list of better stat lines.

    Args:
        better_statlines (list): The list of better stat lines.

    Returns:
        str: The comparator value and the shortened stat comparison list.
    """
    if not better_statlines:
        return [0, []]
    random_number_of_players = random.randint(1, len(better_statlines))

    better_statlines = better_statlines[:random_number_of_players]
    return [
        min([statline["GAME_DATE_EST"] for statline in better_statlines]),
        better_statlines,
    ]


@app.route("/api/v1/stat/pra", methods=["GET"])
def generate_points_rebounds_assists_stat() -> str:
    """
    Generates a string representation of a random Points, Rebounds and Assists (PRA) stat.

    Returns:
        str: String representation of a PRA stat.
    """
    statline = get_random_stat_line("PRA")
    better_statlines = get_better_statlines(statline, "PRA")

    if not better_statlines:
        return f"On {convert_date(statline['GAME_DATE_EST'])}, {statline['PLAYER_NAME']} was the only player since 2004 to score {statline['PTS']} points, grab {statline['REB']} rebounds and deliver {statline['AST']} assists"

    comparator = get_random_date_comparison(better_statlines)
    oldest_statline_date = comparator[0]
    better_statlines = comparator[1]
    suffix = add_suffix(len(better_statlines))

    return f"On {convert_date(statline['GAME_DATE_EST'])}, {statline['PLAYER_NAME']} was the {len(better_statlines)}{suffix} player since {convert_date(oldest_statline_date)} to score {statline['PTS']} points, grab {statline['REB']} rebounds and deliver {statline['AST']} assists."


@app.route("/api/v1/stat/full", methods=["GET"])
def generate_full_statline_stat() -> str:
    """
    Generates a string representation of a random full stat line.

    Returns:
        str: String representation of a full stat line.
    """
    statline = get_random_stat_line("ALL")
    better_statlines = get_better_statlines(statline, "ALL")

    if not better_statlines:
        return f"On {convert_date(statline['GAME_DATE_EST'])}, {statline['PLAYER_NAME']} was the only player since 2004 to score {statline['PTS']} points, grab {statline['REB']} rebounds, deliver {statline['AST']} assists, block {statline['BLK']} shots and get {statline['STL']} steals."

    comparator = get_random_date_comparison(better_statlines)
    oldest_statline_date = comparator[0]
    better_statlines = comparator[1]
    suffix = add_suffix(len(better_statlines))

    return f"On {convert_date(statline['GAME_DATE_EST'])}, {statline['PLAYER_NAME']} was the {len(better_statlines)}{suffix} player since {convert_date(oldest_statline_date)} to score {statline['PTS']} points, grab {statline['REB']} rebounds, deliver {statline['AST']} assists, block {statline['BLK']} shots and get {statline['STL']} steals."


@app.route("/api/v1/stat/ef", methods=["GET"])
def generate_game_effiency_stat():
    """
    Generates a string representation of a random game efficiency stat.

    Returns:
        str: String representation of a game efficiency stat.
    """
    statline = get_random_stat_line("EF")
    better_statlines = get_better_statlines(statline, "EF")

    if not better_statlines:
        return f"On {convert_date(statline['GAME_DATE_EST'])}, {statline['PLAYER_NAME']} was the only player since 2004 to score {statline['PTS']} points, grab {statline['REB']} rebounds, deliver {statline['AST']} assists, block {statline['BLK']} shots and get {statline['STL']} steals while shooting over {round(statline['FG_PCT']*100, 2)} percent from the field."

    comparator = get_random_date_comparison(better_statlines)
    oldest_statline_date = comparator[0]
    better_statlines = comparator[1]
    suffix = add_suffix(len(better_statlines))

    return f"On {convert_date(statline['GAME_DATE_EST'])}, {statline['PLAYER_NAME']} was the {len(better_statlines)}{suffix} player since {convert_date(oldest_statline_date)} to score {statline['PTS']} points, grab {statline['REB']} rebounds, deliver {statline['AST']} assists, block {statline['BLK']} shots and get {statline['STL']} steals while shooting over {round(statline['FG_PCT']*100, 2)} percent from the field."


@app.route("/api/v1/stat/season", methods=["GET"])
def generate_season_stat():
    statline = get_random_season_statline()
    better_statlines = get_better_season_statlines(statline)
    full_length = len(better_statlines)
    if not better_statlines:
        return f"In the {statline['Season']} season, {statline['PLAYER']} was the only player since 1997-1998 to average {statline['PTS']} points, {statline['TRB']} rebounds, and {statline['AST']} assists."

    random_number_of_players = random.randint(1, len(better_statlines))

    better_statlines = better_statlines[:random_number_of_players]
    oldest_season = min([statline["SeasonInt"] for statline in better_statlines])

    if oldest_season == statline["SeasonInt"]:
        return f"In the {statline['Season']} season, {statline['Player'].strip('*')} was one of {full_length} players to average {statline['PTS']} points, {statline['TRB']} rebounds, and {statline['AST']} assists."

    suffix = add_suffix(len(better_statlines))

    return f"In the {statline['Season']} season, {statline['Player'].strip('*')} was the {len(better_statlines)}{suffix} player since {int_to_season[oldest_season]} to average {statline['PTS']} points, {statline['TRB']} rebounds, and {statline['AST']} assists."


if __name__ == "__main__":
    app.run()
