# @author:Xiaotong Wang

import io
from itertools import zip_longest
from urllib.request import Request, urlopen
import pandas as pd
from bs4 import BeautifulSoup
import ssl

pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.width', 1000)  # Increase display width
pd.set_option('display.max_colwidth', None)  # Show full content of each column

# Create unverified SSL context
ssl._create_default_https_context = ssl._create_unverified_context


def extract_game_info(url, source, headers, pages):
    game_scorer, game_names, game_scores, game_comments, scorer_links, scorer_names = [], [], [], [], [], []
    for page in range(1, pages + 1):
        full_url = f'{url}?page={page}'
        req = Request(url=full_url, headers=headers)
        legacy_reviews = urlopen(req)
        soup = BeautifulSoup(legacy_reviews.read(), "html.parser")
        game_review_rows = soup.find_all('div', class_='row review-row py-2')

        for row in game_review_rows:
            # Extract game names
            game_link = row.find('a', href=lambda href: href and '/game/' in href)
            game_name = game_link.get_text(strip=True) if game_link else ''
            game_names.append(game_name)

            # Extract score
            score_span = row.find('span', class_='score-number-bold')
            score = score_span.get_text(strip=True) if score_span else ''
            game_scores.append(score)

            # Extract comments
            comments_element = row.find('p', {'class': 'mb-0 wspw'})
            comment = comments_element.get_text(strip=True) if comments_element else ''
            game_comments.append(comment)

            # Extract scorer's name and link
            scorer_element = row.find('app-author-list')
            scorer_name = scorer_element.get_text(strip=True) if scorer_element else ''
            link_element = scorer_element.find('a', href=True) if scorer_element else None
            full_link = f"https://opencritic.com{link_element['href']}" if link_element else ''

            scorer_names.append(scorer_name)
            scorer_links.append(full_link)
            game_scorer.append(source)

            fout = open('game_raw_data.txt', 'wt',
                        encoding='utf-8')
            fout.write(str(row))
            fout.close()

    return game_names, game_scorer, game_scores, game_comments, scorer_links, scorer_names


# search the input name and generate a txt file that stores the info
def search_data(file_path, user_input):
    # Load the Excel file
    df = pd.read_excel(file_path, engine='openpyxl')
    # Initialize a list to store results
    results = []
    # Iterate through each group of 6 columns
    for i in range(0, 78, 6):
        # Select the columns for this group
        group_columns = df.iloc[:, i:i+6]
        # Search for the user input in the first column of the group
        matched_rows = group_columns[group_columns.iloc[:, 0].str.contains(user_input, case=False, na=False)]
        # Append matched rows to the results
        results.append(matched_rows)

    # Combine all results
    final_results = pd.concat(results)

    # transform results into txt
    buffer = io.StringIO()
    final_results.to_csv(buffer, sep='\t', index=False)
    buffer.seek(0)
    return buffer

# read the search result and make it into dataframe
def clean_data(buffer,input):
    # Parse the data
    parsed_data = []
    for line in buffer:
        if line.strip().lower().startswith(input.lower()):
            # Split the line by tab and filter out empty strings
            split_line = [item.strip() for item in line.split('\t') if item.strip()]
            if split_line:
                parsed_data.append(split_line)
    # Assume the first line of data contains the correct column names
    column_names = parsed_data[0] if parsed_data else []
    df = pd.DataFrame(parsed_data[1:], columns=column_names)
    df.dropna(how='all', inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df



if __name__ == "__main__":
#
# # Configuration
#     headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'}
#     output_file = 'GameReviews.xlsx'
#
# # Extract data
#     gamespot_info = extract_game_info('https://opencritic.com/outlet/32/gamespot', 'Game Spot', headers, 102)
#     gameinformer_info = extract_game_info('https://opencritic.com/outlet/35/game-informer', 'Game Informer', headers, 82)
#     ign_info = extract_game_info('https://opencritic.com/outlet/56/ign','IGN', headers, 106)
#     metrogamecentral_info = extract_game_info('https://opencritic.com/outlet/75/metro-gamecentral', 'Metro GameCentral', headers, 93)
#     eurogamer_info = extract_game_info('https://opencritic.com/outlet/114/eurogamer','Eurogamer', headers,76)
#     destructoid_info = extract_game_info('https://opencritic.com/outlet/90/destructoid', 'Destructoid', headers, 132)
#     waytoomanygames_info = extract_game_info('https://opencritic.com/outlet/742/waytoomanygames', 'WayTooManyGames',headers, 78)
#     gamerescape_info = extract_game_info('https://opencritic.com/outlet/452/gamer-escape', 'Gamer Escape', headers, 28)
#     nichegamer_info = extract_game_info('https://opencritic.com/outlet/298/niche-gamer', 'Niche Gamer', headers, 49)
#     xboxera_info = extract_game_info('https://opencritic.com/outlet/758/xboxera','XboxEra', headers, 28)
#     nintendolife_info = extract_game_info('https://opencritic.com/outlet/136/nintendo-life','Nintendo Life', headers,161)
#     impulsegamer_info = extract_game_info('https://opencritic.com/outlet/31/impulsegamer', 'Impulsegamer', headers, 95)
#     spaziogames_info = extract_game_info('https://opencritic.com/outlet/502/spaziogames','Spaziogames',headers,111)
# # Combining data
#     all_data = zip_longest(*gamespot_info,
#                        *gameinformer_info,
#                        *ign_info,
#                        *metrogamecentral_info,
#                        *eurogamer_info,
#                        *destructoid_info,
#                        *waytoomanygames_info,
#                        *gamerescape_info,
#                        *nichegamer_info,
#                        *xboxera_info,
#                        *nintendolife_info,
#                        *impulsegamer_info,
#                        *spaziogames_info,
#                        fillvalue='')
#     df = pd.DataFrame(all_data, columns=['GameTitle', 'RatingOrganization', 'Ratings', 'ReviewerComments', 'ReviewerProfileLink', 'ReviewerName'] * 13)
#
# # Save to Excel
#     df.to_excel(output_file, index=False)

# Example search usage
    file_path = 'GameReviews.xlsx'
    game_name = 'The Talos Principle 2'

    buffer = search_data(file_path, game_name)
    # Clean the data
    cleaned_df = clean_data(buffer,game_name)
    # Print the cleaned DataFrame to the console
    print(cleaned_df)

