import os
from flask import Flask, jsonify
import requests
import random
from dotenv import load_dotenv

# load all environment variables
load_dotenv()

# Set up the base URL for your API
base_url = os.getenv("supabase_base_url")

# Get the API key from your environment variables
api_key = os.getenv("supabase_api_key")

def get_random_stat_line() -> dict:
    
    # Define the headers including your API key
    headers = {
        "apikey": api_key,
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
    }

    # Generate a random number within the range of total rows
    random_offset = random.randint(0, 50000)

    # Define a maximum number of attempts to avoid infinite loops
    max_attempts = 10000
    attempts = 0
    
    while attempts < max_attempts:
        random_offset = random.randint(0, 50000)
        response = requests.get(
            f"https://xxgcomdjiqkcnbuohybc.supabase.co/rest/v1/Game Logs?offset={random_offset}&AST=lt.10&REB=lt.10&PTS=gt.40&PTS=lt.60&limit=1",
            headers=headers,
        )

        # If the response is not empty, return the record
        if response.json():
            return response.json()[0]
        attempts += 1

    # If we've tried max_attempts times and haven't found a record,
    # raise an exception or return some kind of error indicator
    raise ValueError("Could not find a record after multiple attempts")

def get_better_statlines(statline: dict) -> dict:

    points = statline["PTS"]
    rebounds = statline["REB"]
    assists = statline["AST"]
    date = statline["GAME_DATE_EST"]

    # Define the headers including your API key
    headers = {
        "apikey": api_key,
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
    }
    response = requests.get(
            f"https://xxgcomdjiqkcnbuohybc.supabase.co/rest/v1/Game Logs?GAME_DATE_EST=lt.{date}&PTS=gt.{points}&REB=gt.{rebounds}&AST=gt.{assists}",
            headers=headers,
        )
    
    return response.json()

def generate_points_rebounds_assists_stat() -> str:

    statline = get_random_stat_line()
    better_statlines = get_better_statlines(statline)
    
    random_number_of_players= random.randint(3, min(len(better_statlines), 10))

    better_statlines = better_statlines[:random_number_of_players]
    oldest_statline_date = min([statline['GAME_DATE_EST'] for statline in better_statlines])
    print(oldest_statline_date)
    return f"On {statline['GAME_DATE_EST']}, {statline['PLAYER_NAME']} was the {len(better_statlines)}th player since {oldest_statline_date} to score {statline['PTS']} points, grab {statline['REB']} rebounds and deliver {statline['AST']} assists"

def generate_full_statline_stat() -> str:
    pass

def generate_season_average_stat_totals():
    pass

def generate_season_average_stat_effiency():
    pass

def generate_game_effiency_stat():
    pass

print(generate_points_rebounds_assists_stat())

