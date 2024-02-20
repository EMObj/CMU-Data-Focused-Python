Basic Concept: 
Creates a Python-based application designed to allow video game enthusiasts to search for a game from authentic web data. This tool allows users to view detailed information about various video games, including their description, genre, platform, rating, and user comments. It also includes a powerful search functionality, enabling users to find specific games and learn more about them.

Installation:
1.	Download the .zip file and extract the files inside.
2.	Move all the .py scripts and the .xlsx file into your python environment in your directory.
3.	Import all the required python packages
4.	Run the dfpMain script.
5.	A menu will appear with 5 options.
6.	Choose 1 of the options.
7.	The user will be returned to the main menu after each choice until they decide to QUIT.

Basic User Cases:
Option 1: 
1.	Recommendation by Genre and Platform
2.	When prompted, user gives input of genre and platform
3.	You will then see a dataframe of recommendations

Option 2: Recommendation by Name
1.	When prompted you can input -1 for a full list of games
2.	You will be returned to the main menu and can rechoose 2
3.	When prompted input any name from the list
4.	You will see a list of game titles and descriptions as recommendations

Option 3: Recommendation by Rating
1.	When prompted input a number between 0 and 100
2.	You will see a dataframe of games with higher or equal ratings

Option 4: Review by Name
1.	When prompted input the name of a game
2.	You will see a dataframe with critic reviews of the game

