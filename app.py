import streamlit as st
import pickle 
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=6dd5d25c600b8744fe8363ba7ebfae90&language=en-US".format(movie_id))
    
    if response.status_code == 200:
        data = response.json()
        return "https://image.tmdb.org/t/p/original/" + data["poster_path"]
    else:
        st.error("Error fetching poster. Please try again.")
        return None

def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        poster_url = fetch_poster(movie_id)
        if poster_url:
            recommended_movies_posters.append(poster_url)
    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open("movies_dict.pkl", "rb")) 
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl", "rb"))

st.title("Movie Recommendation System")

# Use an empty string as the default value in selectbox
selected_movie_name = st.selectbox("Name your movie", [''] + movies['title'].tolist())

if st.button("Recommend") and selected_movie_name:
    names, posters = recommend(selected_movie_name)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    image_width = 150  # Adjust the width according to your preference
    text_height = 50  # Adjust the height for movie names
    
    for i, (name, poster) in enumerate(zip(names, posters)):
        with st.expander(f"Movie {i+1}", expanded=True):
            st.text(name)
            st.image(poster, width=image_width)
