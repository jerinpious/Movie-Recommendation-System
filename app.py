import streamlit as st
import pickle
import pandas as pd

def recommend(movie):
    return

movies_list = pickle.load(open('./data/movies.pkl','rb'))
movies_list = movies_list['title'].values

st.title('Movie Recommender')

title_input = st.selectbox(
    'Enter Movie Title',
    movies_list
)

if st.button('Recommend'):
    recommend(title_input)
    st.write(title_input)