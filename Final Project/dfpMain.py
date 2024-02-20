# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 14:23:35 2023

@author: yehuda colton
"""
import pandas as pd
import mobyGames as mg
import webScrappingGames as wsg
import IgdbApiScrape as ias
import OpenCritic as oc

choice = 0

#keeps user in the program until they decide to quit
while (choice != 5):
    
    choice = int(input('Menu: [input the number of your choice]\n'
                       '1. Get recommendations using Genre and Platform.\n'
                       '2. Get recommendations with descriptions using the Name of a game.\n'
                       '3. Get recommendations using a Rating.\n'
                       '4. Get reviews using Name of a game.\n'
                       '5. QUIT\n'))
    
    if (choice == 1):
        #get user input and save as variables
        genre = input('Enter a genre: ')
        platform = input ('Enter a platform: ')
        
        #use input as function parameters for scraping
        rawGameData = mg.scrapeRawGameData(genre, platform)


        #use raw scraped data as function parameter to clean the moby games data
        simplifiedGameData = mg.simplifyGameData(rawGameData)
        
        #put clean data from moby games into a DataFrame
        games = pd.DataFrame(simplifiedGameData, columns = ['Name', 'Moby Score', 'Creation Date','Link'], index = [x for x in range(1, len(simplifiedGameData) + 1)])
        
        #make sure the rows are not truncated
        pd.set_option('display.width', 150)
        pd.set_option('display.max_columns', 500)
        
        print(games)
                
    #########################################
    elif (choice == 2):
        wsg.use()
        
    elif (choice == 3):
        #get user input
        rating = input('Enter a rating between 0 and 100. All games rated higher than this rating will be displayed: ')
        
        #use input in rating search function
        games_data = ias.search_game(ias.client_id, ias.access_token, rating = rating)
       
        #make the data into a DataFrame
        df_games = pd.DataFrame(games_data)
        
        pd.set_option('display.width', 500)
        pd.set_option('display.max_columns', 500)
        
        print(df_games)
        
    elif (choice == 4):
        
        #get user input
        name = input('Enter the name of a game: ')
        
        #use input for function to search games data
        data = oc.search_data('GameReviews.xlsx', name)
        
        # Clean the data
        cleaned_df = oc.clean_data(data, name)

        if cleaned_df.empty:
            print("Cannot find any data about this game. That game might not in the list. Please fix your input and try that again.")
        else:
            print(cleaned_df)

    elif (choice == 5):
        print ('Thank you for using our service, we hope you enjoyed the experience!')
        
        



