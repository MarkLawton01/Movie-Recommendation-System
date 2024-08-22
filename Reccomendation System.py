from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Reading in the data
df = pd.read_excel("Web Scraper/fully_formatted_file.xlsx")
df["combined_features"] = df.apply(lambda row: (" ".join(row["Genre"]) + " ") * 2 + " ".join(row["Cast"]) + " " + row["Director"] + " " + row["Plot Synopsis"], axis=1)

# Preprocessing and vectorization
tfidf_vectorizer = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf_vectorizer.fit_transform(df["combined_features"])

def recommend_movies_with_imdb(input_title, tfidf_matrix=tfidf_matrix, df=df):
    # Movie title not found show user message
    if input_title not in df["Movie Title"].values:
        return f"No movie found with title {input_title}. Please check the title and try again."
    # Getting the index of the movie title the user inputted
    idx = df.index[df["Movie Title"] == input_title].tolist()[0]
    # Calculating the cosine similarities
    cosine_similarities = cosine_similarity(tfidf_matrix[idx], tfidf_matrix).flatten()
    # Getting the IMDB score
    imdb_scores = df["IMDB Score"].values
    # Multiplying the cosine similarities by the IMDB Scores
    combined_scores = cosine_similarities * imdb_scores
    # Sorting the movies in descending order of the combined score
    top_indices = combined_scores.argsort()[-11:-1][::-1]
    # Getting the top 10 movies based on those sorted indices
    top_movies = df.loc[top_indices, ["Movie Title"]]
    return top_movies

def recommended_with_rotten_tomatoes_audience_score(input_title, tfidf_matrix=tfidf_matrix, df=df):
    # Movie title not found show user message
    if input_title not in df["Movie Title"].values:
        return None
    idx = df.index[df["Movie Title"] == input_title].tolist()[0]
    # Calculating the cosine similarities
    cosine_similarities = cosine_similarity(tfidf_matrix[idx], tfidf_matrix).flatten()
    # Getting the Audience Score
    rt_scores = df["Audience Score"].values
    # Multiplying the cosine similarities by the Audience Scores
    combined_scores = cosine_similarities * rt_scores
    # Sorting the movies in descending order of the combined score
    top_indices = combined_scores.argsort()[-11:-1][::-1]
    # Getting the top 10 movies based on those sorted indices
    top_movies = df.loc[top_indices, ["Movie Title"]]
    return top_movies

def recommended_with_rotten_tomatoes_critic_score(input_title, tfidf_matrix=tfidf_matrix, df=df):
    # Movie title not found show user message
    if input_title not in df["Movie Title"].values:
        return None
    idx = df.index[df["Movie Title"] == input_title].tolist()[0]
    # Calculating the cosine similarities
    cosine_similarities = cosine_similarity(tfidf_matrix[idx], tfidf_matrix).flatten()
    # Getting the Critic Score
    rt_scores = df["Critic Score"].values  # Ensure this column exists in your DataFrame
    # Multiplying the cosine similarities by the Critic Scores
    combined_scores = cosine_similarities * rt_scores
    # Sorting the movies in descending order of the combined score
    top_indices = combined_scores.argsort()[-11:-1][::-1]
    # Getting the top 10 movies based on those sorted indices
    top_movies = df.loc[top_indices, ["Movie Title"]]
    return top_movies

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    title = request.form["movie_title"]
    # Getting whether the user wants to use IMDB or Rotten Tomatoes
    recommendation_type = request.form.get("recommendation_type")
    if recommendation_type == "imdb":
        recommendations = recommend_movies_with_imdb(title)
    elif recommendation_type == "rotten_tomatoes_audience":
        recommendations = recommended_with_rotten_tomatoes_audience_score(title)
    elif recommendation_type == "rotten_tomatoes_critic":
        recommendations = recommended_with_rotten_tomatoes_critic_score(title)
    else:
        recommendations = None

    movies = recommendations["Movie Title"].values.tolist()
    return render_template("recommendations.html", movies=movies, title=title, type=recommendation_type)

@app.route("/movie/<title>")
def movie_details(title):
    # Looking for the movie in the DataFrame
    movie_data = df[df["Movie Title"].str.lower() == title.lower()].iloc[0]
    if movie_data.empty:
        return f"No details found for {title}.", 404
    # Passing all the details to the movie_details template
    return render_template("movie_details.html", movie=movie_data)

if __name__ == "__main__":
    app.run(debug=True)
