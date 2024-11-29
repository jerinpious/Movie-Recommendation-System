import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch movie poster from TMDB API
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        response = requests.get(url)
        data = response.json()
        poster_path = data.get('poster_path', '')  # Ensure 'poster_path' exists
        if poster_path:
            full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
            return full_path
        else:
            return "https://via.placeholder.com/500x750.png?text=No+Image+Available"  # Fallback image
    except Exception:
        return "https://via.placeholder.com/500x750.png?text=Error+Fetching+Poster"

# Function to recommend movies
def recommend(movie):
    index = movies_df[movies_df['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movie_names = []
    recommended_movie_posters = []
    
    for i in distances[1:6]:  # Top 5 recommendations
        movie_id = movies_df.iloc[i[0]].movie_id  # Access `movie_id` from DataFrame
        recommended_movie_names.append(movies_df.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    
    return recommended_movie_names, recommended_movie_posters

# Load the movies DataFrame and similarity matrix
movies_df = pickle.load(open('./data/movies.pkl', 'rb'))  # Keep movies as DataFrame
movies = movies_df['title'].values  # Extract titles for dropdown
similarity = pickle.load(open('./data/similarity.pkl', 'rb'))

# Streamlit app interface
st.title('Movie Recommender System')

# Dropdown for movie selection
title_input = st.selectbox(
    'Select or Type a Movie Title',
    movies
)

# Display recommendations when button is clicked
if st.button('Show Recommendations'):
    recommended_movie_names, recommended_movie_posters = recommend(title_input)
    
    # Dynamically display recommendations in a grid
    cols = st.columns(5)  # Create 5 columns for the recommendations
    for col, name, poster in zip(cols, recommended_movie_names, recommended_movie_posters):
        with col:
            st.text(name)
            st.image(poster)
