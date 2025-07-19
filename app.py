import os
import gdown

# === similarity.pkl ===
sim_file_id = "1U3LFp0odvw4gW--zMUzOr3gDz3JMmeAY"
sim_url = f"https://drive.google.com/uc?id={sim_file_id}"

if not os.path.exists("similarity.pkl"):
    print("Downloading similarity.pkl from Google Drive...")
    gdown.download(sim_url, "similarity.pkl", quiet=False)

# === movies.pkl ===
movies_file_id = "1aFxigv2TD7cdDt4N_PgU7vPh16aruLNv"
movies_url = f"https://drive.google.com/uc?id={movies_file_id}"

if not os.path.exists("movies.pkl"):
    print("Downloading movies.pkl from Google Drive...")
    gdown.download(movies_url, "movies.pkl", quiet=False)


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
