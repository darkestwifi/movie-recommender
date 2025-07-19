import os
import gdown

file_id = "1U3LFp0odvw4gW--zMUzOr3gDz3JMmeAY"
url = f"https://drive.google.com/uc?id={file_id}"

# Download similarity.pkl if it doesn't already exist
if not os.path.exists("similarity.pkl"):
    print("Downloading similarity.pkl from Google Drive...")
    gdown.download(url, "similarity.pkl", quiet=False)


import streamlit as st
import pickle

# Load saved data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Function to recommend
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    return [movies.iloc[i[0]].title for i in movie_list]

# Streamlit UI
st.title("Movie Recommender System")
selected_movie_name = st.selectbox("Select a movie", movies['title'].values)

if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    st.write("Top 5 Recommendations:")
    for i in recommendations:
        st.write(i)
