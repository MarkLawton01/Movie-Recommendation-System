import random
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Headers to mimic a browser visit
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


def formatExcel():
    # Reading in the excel file
    file = pd.read_excel("IMDB_Scraper.xlsx")
    # https://www.rottentomatoes.com/m/

    # Removing the rows where the IMDB Rating had "No Rating"
    file["IMDB Score"] = pd.to_numeric(file["IMDB Score"], errors='coerce')
    file = file.dropna()
    file["IMDB Score"] = file["IMDB Score"].astype(float)

    # Formatting the movie titles
    movie_titles_lower_case = file["Movie Title"].str.lower()
    movie_titles_spaces_replaced = movie_titles_lower_case.str.replace(" ", "_")
    special_characters_removed = movie_titles_spaces_replaced.str.replace("[^a-zA-Z0-9_]", "", regex=True)

    file["Formatted Title"] = special_characters_removed
    # Returning both they year and dates
    return file


def selenium(data):
    driver = webdriver.Chrome()
    audience_scores = []
    critic_scores = []

    try:
        # Looping through the both the index and the row of the excel sheet
        for index, row in data.iterrows():
            movie_name = row["Formatted Title"]
            imdb_year = str(row["Year"])
            url = f'https://web.archive.org/web/20240329160702/https://www.rottentomatoes.com/m/{movie_name}'

            driver.get(url)
            wait = WebDriverWait(driver, 10)

            try:
                # Getting the year
                time_tag = wait.until(EC.presence_of_element_located((By.TAG_NAME, "time")))
                year = time_tag.text.split(",")[1].strip()

                # Making sure the year scraped from rotten tomatoes matches the year from IMDB
                if (year != imdb_year):
                    # If not modify the link to try to find the correct movie
                    url = f'https://web.archive.org/web/20240329160702/https://www.rottentomatoes.com/m/{movie_name}_{imdb_year}'
                    driver.get(url)
                    wait = WebDriverWait(driver, 10)

                # Getting the audience and critic scores
                score_board = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "thumbnail-scoreboard-wrap")))
                l = score_board.text.split("\n")
                audience_score = l[3]
                critic_score = l[6]
                print(audience_score, critic_score)
            except Exception as e:
                # For error checking
                print(f"Failed to retrieve scores for {movie_name}: {str(e)}")
                # Assigning values to nothing if failed to find scores
                audience_score = None
                critic_score = None

            # Append scores to lists regardless of whether an exception was raised
            audience_scores.append(audience_score)
            critic_scores.append(critic_score)

    finally:
        driver.quit()

    # Assign the scores to the DataFrame only after ensuring they match the DataFrame's length
    data['Audience Score'] = audience_scores
    data['Critic Score'] = critic_scores

    return data


def saveUpdatedExcel(data):
    # Save the updated DataFrame back to Excel
    data.to_excel("All_Data.xlsx", index=False)

def data_cleaning():
    # Reading in the File
    file = pd.read_excel("All_Data.xlsx")
    # Getting rid of any rows that contain blank spaces
    file = file.dropna()
    # Removing percentage symbol
    file["Critic Score"] = file["Critic Score"].str.strip("%")
    file["Audience Score"] = file["Audience Score"].str.strip("%")
    # Convert to numeric which turns all non-numeric values to NaN
    file["Critic Score"] = pd.to_numeric(file["Critic Score"], errors='coerce')
    file["Audience Score"] = pd.to_numeric(file["Audience Score"], errors='coerce')
    # Dropping all rows where cells contain NaN values
    file = file.dropna()
    # Converting values in each column to an integer
    file["Critic Score"] = file["Critic Score"].astype(int)
    file["Audience Score"] = file["Audience Score"].astype(int)

    file.to_excel("fully_formatted_file.xlsx", index=False)


def main():
    data = formatExcel()
    updated_data = selenium(data)
    saveUpdatedExcel(updated_data)
    data_cleaning()


if __name__ == "__main__":
    main()


