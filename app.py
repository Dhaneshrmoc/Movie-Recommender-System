import streamlit as st
import pickle as pic
import pandas as pd
import requests

movies_dict = pic.load(open('movie_dict.pkl','rb'))
movie_name = pd.DataFrame(movies_dict)
simi = pic.load(open('similarity.pkl', 'rb'))
st.title('Movie Recommender System')
option = st.selectbox(
    "Which movie do you like?",
    movie_name['title'].values
)


def fetch_poster(movie_id):
    api_key = "8b8298c9c05655f3861ddc33b34f5b06%20- "
    url = f"https://webservice.fanart.tv/v3/movies/{movie_id}?api_key={api_key}"

    response = requests.get(url)
    data = response.json()

    if "movieposter" in data and isinstance(data["movieposter"], list) and len(data["movieposter"]) > 0:
        return data["movieposter"][0]["url"]
    return "https://via.placeholder.com/500x750?text=No+Image"


def recommend(movie):
    movie_index = movie_name[movie_name['title'] == movie].index[0]
    movie_list = sorted(list(enumerate(simi[movie_index])), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movie_list:
        movie_id = movie_name.iloc[i[0]].movie_id
        recommended_movies.append(movie_name.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies , recommended_movies_posters

if st.button('Recommend'):

    name , poster = recommend(option)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(name[0])
        st.image(poster[0])
    with col2:
        st.text(name[1])
        st.image(poster[1])
    with col3:
        st.text(name[2])
        st.image(poster[2])
    with col4:
        st.text(name[3])
        st.image(poster[3])
    with col5:
        st.text(name[4])
        st.image(poster[4])