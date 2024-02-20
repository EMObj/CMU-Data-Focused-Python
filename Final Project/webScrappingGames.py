#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 11:21:22 2023

@author: vanessaj
"""

import requests
from bs4 import BeautifulSoup
import re

def get_user_input():
    print("If you want to see the list of games that we have recommendations for enter -1")
    game = input("Enter in a game you like to play and if it is on our list, we will recommend a few others\n")
    return game

def scrape_for_inner_a_href_tags_for_game_titles(element):
    game_titles = []
    all_inner_tags = element.find_all(recursive=False)

    if all_inner_tags != None:
        for tag in all_inner_tags:
            if tag.name == "a" and tag.get("href"):
                game_titles.append(tag.text)
            game_titles.extend(scrape_for_inner_a_href_tags_for_game_titles(tag))
    return game_titles

#get the list of all the "Game Like -insert name here-" 
def get_games_that_have_recs_list(inputted_game_like):
    try:
        url = "https://gameslikefinder.com/" + inputted_game_like[0].lower().replace(" ","-")
        headers = {'User-Agent': 'Mozilla/5.0 (Platform; Security; OS-or-CPU; Localization; rv:1.4) Gecko/20030624 Netscape/7.1 (ax)'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text,'html.parser')
            game_like_names = soup.find("div", id = "gp-site-wrapper")
            game_titles_list = scrape_for_inner_h2_game_tags_to_get_recommended_game_titles(game_like_names)
            games_description_list = scrape_for_inner_descriptions_of_recommended_game_titles(game_like_names)
        return game_titles_list, games_description_list
    except:
        print("That game is not in the list!")
        return [],[]
        
#scrapes the page of the specific game entered by the user to get the recommended games
def scrape_for_inner_h2_game_tags_to_get_recommended_game_titles(element):
    game_titles = []
    all_inner_tags = element.find_all(recursive=False)

    if all_inner_tags != None:
        for tag in all_inner_tags:
            if tag.name == "h2":
                game_titles.append(tag.text)
            game_titles.extend(scrape_for_inner_h2_game_tags_to_get_recommended_game_titles(tag))
    return game_titles

def scrape_for_inner_descriptions_of_recommended_game_titles(element):
    game_descriptions = []
    all_inner_tags = element.find_all(recursive=False)
    if all_inner_tags != None:
        for tag in all_inner_tags:
            if tag.name == "p":
                game_descriptions.append(tag.text)
            game_descriptions.extend(scrape_for_inner_descriptions_of_recommended_game_titles(tag))
    return game_descriptions

    
#gets the list of "Games like -insert game name here-"
def get_games_like_list():
    url = "https://gameslikefinder.com/games-like-directory/"
    headers = {'User-Agent': 'Mozilla/5.0 (Platform; Security; OS-or-CPU; Localization; rv:1.4) Gecko/20030624 Netscape/7.1 (ax)'}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text,'html.parser')
        game_like_names = soup.find("div", id = "gp-site-wrapper")
        game_titles_list = scrape_for_inner_a_href_tags_for_game_titles(game_like_names)[16:]
        game_titles_list = game_titles_list[0:-4]
        return game_titles_list
    
#displays the list of games that there are available recommendations
def list_all_games_that_have_recommendations(entered_list):
    print()
    print("The games we have recommendations for are")
    for game in entered_list:
        game_name = re.search(r'(?<=Like ).*', game)
        print(game_name.group(0))
    

#displays the recommendations and their descriptions
def display_the_recommendations_and_their_descriptions(recommendations, their_descriptions):
    if len(recommendations) != 0:
        print()
        print("Your recommendations and their descriptions are:")
        for x in range(len(recommendations)):
            print(recommendations[x] +":")
            description = re.search(r'.*(?=\s?\[)', their_descriptions[x])
            print(description.group(0))
            print()
    else:
        print("Therefore we don't have any recommendations for you! Sorry!")
        
#get user input about a game they like
def use():
    picked_user_game = get_user_input()
    
    #the list of "Games Like -insert game name here-" that is on the website being scrapped
    games_like = get_games_like_list()
    #check to see if the game that the user asked about is in the list
    if(picked_user_game != "-1"):
        games_like_inputted_game_title = [x for x in games_like if picked_user_game.lower() in x.lower()]
    
        #getting the recommendations of the games that are like the inputted game from the user
        games_like_the_inital_game_that_was_entered, their_descriptions = get_games_that_have_recs_list(games_like_inputted_game_title)
    
        display_the_recommendations_and_their_descriptions(games_like_the_inital_game_that_was_entered, their_descriptions)
    else:
        list_all_games_that_have_recommendations(games_like)




