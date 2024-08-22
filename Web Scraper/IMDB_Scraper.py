import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
import random


# Headers to mimic a browser visit
HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}


def create_movie_dict(movie_title, cast, genre, synopsis, score, director, year):
    movie_dict = {
        "Movie Title": movie_title,
        "Cast": cast,
        "Genre": genre,
        "Plot Synopsis": synopsis,
        "IMDB Score": score,
        "Director": director,
        "Year": year
    }
    return movie_dict


def get_genre_page_links():
    # Link to movie by genre page
    url = "https://www.imdb.com/feature/genre/?ref_=nv_ch_gr"

    # Send a request to the URL with headers
    response = requests.get(url, headers=HEADER)
    doc = BeautifulSoup(response.text, "html.parser")

    # Webpage container storing each category by genre
    genre_container = doc.find_all("div", class_="ipc-chip-list__scroller")
    movie_genre_container = genre_container[1]

    # List to store the links to each page of movie lists
    genre_overview_links = []

    # Looping through each genre in the genre container
    for genre in movie_genre_container.find_all("a", class_="ipc-chip ipc-chip--on-base-accent2"):
        # Getting the link to page that contains the movie list of each genre
        genre_links = genre.get("href")
        genre_full_link = "https://www.imdb.com" + genre_links

        # Adding each page to the container
        genre_overview_links.append(genre_full_link)

    return genre_overview_links


def get_individual_movie_page_links(genre_link_list):
    # Using a set to store the movie pages to ensure uniqueness
    individual_movie_page_links = set()

    # Looping through each genre category and getting all the movie links on each page
    for genre in genre_link_list:
        response_2 = requests.get(genre, headers=HEADER)
        doc_2 = BeautifulSoup(response_2.text, "html.parser")
        movie_title_link = doc_2.find_all("a", class_="ipc-title-link-wrapper")

        # Looping through each movie on the page to extract the movie links
        for movie in movie_title_link:
            individual_movie_link = "https://www.imdb.com" + movie.get("href")
            fixed = individual_movie_link.split("_")
            individual_movie_page_links.add(fixed[0])

    return individual_movie_page_links


def gather_movie_information(list_of_movie_links):
    all_movie_data = []

    # Looping through each movie page in the list of movies
    for link in list_of_movie_links:
        response = requests.get(link, headers=HEADER)
        individual_movie_page = BeautifulSoup(response.text, "html.parser")

        # Collecting the necessary data from each of the movie pages
        # Movie Title
        movie_title_tag = individual_movie_page.find("span", class_="hero__primary-text")
        movie_title = movie_title_tag.text

        # Cast members
        cast_tag = individual_movie_page.find_all("a", class_="sc-bfec09a1-1 gCQkeh")
        cast = []
        for cast_member in cast_tag:
            cast.append(cast_member.text)

        # IMDB Score
        IMDB_Score_tag = individual_movie_page.find("span", class_="sc-bde20123-1 cMEQkK")
        if IMDB_Score_tag is None:
            IMDB_Score = "No Rating"
        else:
            IMDB_Score = IMDB_Score_tag.text

        genres = individual_movie_page.find_all("a", href=re.compile("/search/title\?genres="))
        genre_list = []
        for genre in genres:
            genre_list.append(genre.text)

        # Director
        director_tag = individual_movie_page.find("a",
                                                  class_="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link")
        director = director_tag.text

        # Plot Summary
        plot_summary_tag = individual_movie_page.find("span", class_="sc-7193fc79-2 kpMXpM")
        plot_summary = plot_summary_tag.string
        print(plot_summary)

        # Year
        year_tag = individual_movie_page.find_all("a", class_="ipc-link ipc-link--baseAlt ipc-link--inherit-color")
        year_found = False
        for tag in year_tag:
            if len(tag.text) == 4:
                print(tag.text)
                year = tag.text
                year_found = True
        if year_found is False:
            print(f"{movie_title} - year could not be found")
            year = 0

        # Creating a dictionary for each movie, adding each dictionary to a list
        movie_dict = create_movie_dict(movie_title, cast, genre_list, plot_summary, IMDB_Score, director, year)
        all_movie_data.append(movie_dict)

        print(movie_title)
        random_time = random.randint(1, 30)
        print(random_time)
        time.sleep(random_time)

    return all_movie_data

def main():
    genre_link_list = get_genre_page_links()
    individual_movie_page_links = get_individual_movie_page_links(genre_link_list)
    movie_dict = gather_movie_information(individual_movie_page_links)
    movie_df = pd.DataFrame(movie_dict)
    excel_file_path = 'IMDB_Scraper.xlsx'

    # Export the DataFrame to an Excel file
    movie_df.to_excel(excel_file_path, index=False)

if __name__ == '__main__':
    main()
