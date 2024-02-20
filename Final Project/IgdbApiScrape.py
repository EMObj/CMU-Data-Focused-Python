import requests
from requests import post
import pandas as pd


# Twitch OAuth token URL
url = 'https://id.twitch.tv/oauth2/token'

# Your Client ID and Client Secret
client_id = 'v03flev5gy72g55i170au4kbcdtibf'
client_secret = 'irnayifr3q0vx2le9yifq412n0tbtx'

# Formulate the request
body = {
    'client_id': client_id,
    'client_secret': client_secret,
    'grant_type': 'client_credentials'
}

# Make the POST request
response = requests.post(url, data=body)

# Extracting the access token from the response
if response.status_code == 200:
    token = response.json().get('access_token')
    #print("Access Token:", token)
else:
    print("Failed to get the access token:", response.status_code)

import requests

# URL for the IGDB API endpoint
url = 'https://api.igdb.com/v4/age_ratings'

# Headers containing the Client ID and Authorization token
headers = {
    'Client-ID': 'v03flev5gy72g55i170au4kbcdtibf',  # Replace with your Client ID
    'Authorization': 'Bearer oycr7mauajv4daqng81vdn4y5zeaa2'  # Replace with your Access Token
}

# The data/payload of your request
data = 'fields category,checksum,content_descriptions,rating,rating_cover_url,synopsis;'

# Make the POST request
response = requests.post(url, headers=headers, data=data)

# Check if the request was successful
#if response.status_code == 200:
    # Print the JSON response
    #print("Response:", response.json())
#else:
    #print("Failed to retrieve data. Status Code:", response.status_code)



# Fetch data from IGDB API
url = 'https://api.igdb.com/v4/age_ratings'
headers = {
    'Client-ID': 'v03flev5gy72g55i170au4kbcdtibf',
    'Authorization': 'Bearer no4q3kea3km7cpgiywzdy2ipd8mg96'
}

data = 'fields category,checksum,content_descriptions,rating,rating_cover_url,synopsis;'

response = requests.post(url, headers=headers, data=data)

if response.status_code != 200:
    print("Failed to retrieve data. Status Code:", response.status_code)
    exit()

# Convert to DataFrame
api_data = pd.DataFrame(response.json())

# Output to Excel
api_data.to_excel('output_raw_data.xlsx', index=False, engine='openpyxl')

# Request body
# 'fields' are the data fields you want from the API
# Adjust the query to fetch the game name, rating, comments, and category

import requests
import json

# Twitch API credentials
client_id = 'v03flev5gy72g55i170au4kbcdtibf'  # Replace with your actual Client ID
access_token = '3sl7clppzfj3mwhvexds1h9vrvmm43'  # Replace with your actual Access Token

# IGDB API endpoint for the games
url = 'https://api.igdb.com/v4/games/'

# Headers for authorization
headers = {
    'Client-ID': client_id,
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

# The body of the request, asking for all fields for game with different ID
body = 'fields *; where id = 1;'

# Make the POST request to the IGDB API
response = requests.post(url, headers=headers, data=body)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response to JSON
    game_info = response.json()
    # Print the retrieved game information
    #print(json.dumps(game_info, indent=4))
else:
    print(f"Failed to retrieve data. Status Code: {response.status_code}, Response: {response.text}")

def clean_game_data(raw_data):
    # Prepare cleaned data
    cleaned_data = []
    for game in raw_data:
        game_entry = {
            'Name': game.get('name'),
            'Genres': ', '.join([genre['name'] for genre in game.get('genres', []) if genre.get('name')]),
            'Platforms': ', '.join([platform['name'] for platform in game.get('platforms', []) if platform.get('name')]),
            'Rating': game.get('rating')
        }
        cleaned_data.append(game_entry)
    return cleaned_data

def search_game(client_id, access_token, rating=None):
    url = 'https://api.igdb.com/v4/games/'
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    query_parts = ['fields name, genres.name, rating, platforms.name;']
    if rating:
        query_parts.append(f'where rating >= {rating};')

    body = ' '.join(query_parts)
    response = requests.post(url, headers=headers, data=body)

    if response.status_code == 200:
        raw_data = response.json()
        cleaned_data = clean_game_data(raw_data)
        return cleaned_data
    else:
        raise Exception(f"Failed to retrieve data. Status Code: {response.status_code}, Response: {response.text}")

# # Example usage
#client_id = 'v03flev5gy72g55i170au4kbcdtibf'
#access_token = 'no4q3kea3km7cpgiywzdy2ipd8mg96'
#games_data = search_game(client_id, access_token, rating=89)

# Convert the cleaned data to a DataFrame
#df_games = pd.DataFrame(games_data)

# Output the DataFrame to an Excel file, if needed
#df_games.to_excel('cleaned_games_data.xlsx', index=False, engine='openpyxl')

# Print the DataFrame
#print(df_games)
