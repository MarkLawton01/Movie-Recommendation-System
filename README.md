# 🎬 Movie Recommendation System (with Web Scraping and API Integration) 🎬

## Overview
This project implements a movie recommendation system that combines data from **IMDb** and **Rotten Tomatoes** to provide users with customized movie recommendations. The project was built using **Python**, **Selenium**, **BeautifulSoup**, and **Flask** to create a web-based interface for users to input movie titles and receive recommendations based on various criteria (IMDb scores, Rotten Tomatoes critic and audience scores).

Due to frequent changes in the structures of the IMDb and Rotten Tomatoes websites, this project demonstrates the challenges of maintaining a web scraper in a real-world scenario. This README also outlines how future iterations would adapt to these changes using more robust and sustainable methods such as APIs and Neo4j databases.

## Project Components

- **IMDb Web Scraper**:
  - Scrapes movie data from IMDb, including titles, genres, cast, director, IMDb scores, and plot summaries.
  - Gathers a comprehensive dataset, which is then used for building a recommendation engine.

- **Rotten Tomatoes Web Scraper**:
  - Scrapes additional scores (critic and audience) from Rotten Tomatoes.
  - This data is used to enhance the recommendations by offering different scoring perspectives.

- **Recommendation Engine**:
  - A content-based recommendation system built using **TF-IDF Vectorization** and **Cosine Similarity**.
  - Users can choose between recommendations based on IMDb scores, Rotten Tomatoes Audience scores, or Rotten Tomatoes Critic scores.

- **Flask Web App**:
  - A simple front-end web interface where users can input a movie title and choose the type of recommendation they want to receive.
  - Displays the top 10 recommended movies based on the input criteria.

## Technical Details

- **Web Scraping Libraries**: `BeautifulSoup`, `Selenium`
- **Vectorization**: `TfidfVectorizer` from `scikit-learn`
- **Recommendation Algorithm**: `Cosine Similarity` on combined movie features (genre, cast, director, plot synopsis)
- **Data Handling**: `pandas` for data manipulation and cleaning
- **Web Framework**: `Flask`
- **Excel Handling**: Data is read from and written to Excel files using `pandas`.


