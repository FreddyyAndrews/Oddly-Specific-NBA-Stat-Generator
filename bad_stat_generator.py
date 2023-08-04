import math
import os
from flask import Flask, jsonify
import requests
import random
from dotenv import load_dotenv

load_dotenv()
base_url = os.getenv("supabase_base_url")
api_key = os.getenv("supabase_api_key")

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
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
    }
    endpoint = ""
    if caller == "PRA":
        endpoint = "/rest/v1/Game Logs?PTS=gte.45&AST=gte.3&REB=gte.3&GAME_DATE_EST=gte.2010-01-01"

    if caller == "ALL":
        endpoint = "/rest/v1/Game Logs?PTS=gte.40&AST=gte.3&REB=gte.3&BLK=gte.2&STL=gte.2&GAME_DATE_EST=gte.2010-01-01"

    if caller == "EF":
        endpoint = "/rest/v1/Game Logs?PTS=gte.25&AST=gte.2&REB=gte.2&BLK=gte.2&STL=gte.2&FG_PCT=gte.0.5&GAME_DATE_EST=gte.2010-01-01"

    response = requests.get(
            f"{base_url}{endpoint}",
            headers=headers,
        )

    if response.json():
        response_dict = response.json()
        return response_dict[random.randint(0, len(response_dict) -1)]
    else:
        raise ValueError("Could not find a record.")

def get_better_statlines(statline: dict, caller: str) -> dict:
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
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
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

def add_suffix(n):
    """Add a suffix to an integer."""
    suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
    
    if 10 <= n <= 20:
        return 'th'
    
    return suffixes.get(n % 10, 'th')

def get_random_date_comparison(better_statlines: list):
    """
    Gets a random comparator value from a list of better stat lines.

    Args:
        better_statlines (list): The list of better stat lines.
    
    Returns:
        str: The comparator value.
    """
    random_number_of_players= random.randint(math.floor(len(better_statlines)/2), len(better_statlines))
    better_statlines = better_statlines[:random_number_of_players]
    return min([statline['GAME_DATE_EST'] for statline in better_statlines])

def generate_points_rebounds_assists_stat() -> str:
    """
    Generates a string representation of a random Points, Rebounds and Assists (PRA) stat.

    Returns:
        str: String representation of a PRA stat.
    """
    statline = get_random_stat_line("PRA")
    better_statlines = get_better_statlines(statline, "PRA")

    if not better_statlines:
        return f"On {statline['GAME_DATE_EST']}, {statline['PLAYER_NAME']} was the only player since 2004 to score {statline['PTS']} points, grab {statline['REB']} rebounds and deliver {statline['AST']} assists"
    
    oldest_statline_date = get_random_date_comparison(better_statlines)
    suffix = add_suffix(len(better_statlines))

    return f"On {statline['GAME_DATE_EST']}, {statline['PLAYER_NAME']} was the {len(better_statlines)}{suffix} player since {oldest_statline_date} to score {statline['PTS']} points, grab {statline['REB']} rebounds and deliver {statline['AST']} assists."

def generate_full_statline_stat() -> str:
    """
    Generates a string representation of a random full stat line.

    Returns:
        str: String representation of a full stat line.
    """
    statline = get_random_stat_line("ALL")
    better_statlines = get_better_statlines(statline, "ALL")

    if not better_statlines:
        return f"On {statline['GAME_DATE_EST']}, {statline['PLAYER_NAME']} was the only player since 2004 to score {statline['PTS']} points, grab {statline['REB']} rebounds, deliver {statline['AST']} assists, block {statline['BLK']} shots and get {statline['STL']} steals."
    
    oldest_statline_date = get_random_date_comparison(better_statlines)
    suffix = add_suffix(len(better_statlines))

    return f"On {statline['GAME_DATE_EST']}, {statline['PLAYER_NAME']} was the {len(better_statlines)}{suffix} player since {oldest_statline_date} to score {statline['PTS']} points, grab {statline['REB']} rebounds, deliver {statline['AST']} assists, block {statline['BLK']} shots and get {statline['STL']} steals."

def generate_game_effiency_stat():
    """
    Generates a string representation of a random game efficiency stat.

    Returns:
        str: String representation of a game efficiency stat.
    """
    statline = get_random_stat_line("EF")
    better_statlines = get_better_statlines(statline, "EF")

    if not better_statlines:
        return f"On {statline['GAME_DATE_EST']}, {statline['PLAYER_NAME']} was the only player since 2004 to score {statline['PTS']} points, grab {statline['REB']} rebounds, deliver {statline['AST']} assists, block {statline['BLK']} shots and get {statline['STL']} steals while shooting over {round(statline['FG_PCT']*100, 2)} percent from the field."
    
    oldest_statline_date = get_random_date_comparison(better_statlines)
    suffix = add_suffix(len(better_statlines))

    return f"On {statline['GAME_DATE_EST']}, {statline['PLAYER_NAME']} was the {len(better_statlines)}{suffix} player since {oldest_statline_date} to score {statline['PTS']} points, grab {statline['REB']} rebounds, deliver {statline['AST']} assists, block {statline['BLK']} shots and get {statline['STL']} steals while shooting over {round(statline['FG_PCT']*100, 2)} percent from the field."


