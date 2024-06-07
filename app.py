import streamlit as st
import pickle
import pandas as pd
import requests

def fetchPoster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id))
    data = response.json()
    return "http://image.tmdb.org/t/p/w500/"+data['poster_path']

def recommend(movie):
    movies_idx = movies[movies['title'] == movie].index[0]
    distances = similarity[movies_idx]
    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommended = []
    recommendedPosters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id

        recommended.append(movies.iloc[i[0]].title)
        recommendedPosters.append(fetchPoster(movie_id))
    
    return recommended,recommendedPosters


movies_dict = pickle.load(open("movies.pkl","rb"))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity_score.pkl","rb"))

st.title("Movie Recommender System")

selectedMovie = st.selectbox("Select a movie:",
                      movies['title'].values)

if st.button("Recommend"):
    name,posters = recommend(selectedMovie)

    print(posters[0])
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(name[0])
        st.image(posters[0])
    with col2:
        st.markdown(name[1])
        st.image(posters[1])
    with col3:
        st.markdown(name[2])
        st.image(posters[2])
    with col4:
        st.markdown(name[3])
        st.image(posters[3])
    with col5:
        st.markdown(name[4])
        st.image(posters[4])