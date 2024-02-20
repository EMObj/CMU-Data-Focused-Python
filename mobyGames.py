# @author shsong

from urllib.request import Request, urlopen
from bs4 import BeautifulSoup # python3 -m pip install bs4
import json


# Scrapes raw data about games from mobygames.
# Returns a string in JSON format w/ this data.
# Depending on filters from user-inputted params, 
# number of games is 18 or less
'''
Sample Calls:
scrapeRawGameData()
scrapeRawGameData("action")
scrapeRawGameData(platform="windows")
scrapeRawGameData("action", "android")
'''
def scrapeRawGameData(genre=None, platform=None):
    urlStr = buildUrlStr(genre, platform)
    req = Request(
        url=urlStr, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    html = urlopen(req)
    bsyc = BeautifulSoup(html.read(), 'html.parser')

    # Grab the raw game data from the table on this page
    gameTable = bsyc.find('game-browser')
    rawGames = gameTable.attrs[":initial-values"]
    return rawGames


'''
URL TYPES:
Baseline:   'https://www.mobygames.com/game/'
Genre:      'https://www.mobygames.com/game/genre:action/sort:moby_score/page:1/'
Platform:   'https://www.mobygames.com/game/platform:android/sort:moby_score/page:1/'
G + P       'https://www.mobygames.com/game/genre:action/platform:windows/sort:moby_score/page:1/'
'''
# Construct URL str w/ user-inputted params
def buildUrlStr(genre=None, platform=None):
    url = 'https://www.mobygames.com/game/'
    if genre is not None:
        url += f'genre:{genre}/'
    if platform is not None:
        url += f'platform:{platform}/'
    url += 'sort:moby_score/page:1/'
    return url


# Takes outputted str from scrapeRawGameData() and pulls out only the data 
# we want about each game (title, rating, creation date, URL to more info).
# Final format is a 2D list, each internal list contains 
# these 4 fields for a different game.
def simplifyGameData(rawGames):
    # Convert rawGames to json so that we can access direct game data inside.
    # games is a list of 18 dicts - each dict holds one game's data
    games = json.loads(rawGames)["games"]
    # Extract just the fields we want from each game
    simplifiedGameList = [[game["title"], game["moby_score"], 
                           game["created"], game["internal_url"]]
                          for game in games]
    return simplifiedGameList


'''
HOW TO USE THIS FILE IN MAIN PY FILE:
Call scrapeRawGameData() w/ user-inputted params, save to var
Call simplifyGameData() with output from above method, save to var
    This is the final output
Do with this list what you want in the main file
'''