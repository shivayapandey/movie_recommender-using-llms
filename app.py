

# '''
# Author: Shivaya Pandey
# Email: pandeyshivaya@gmail.com
# Date: 2024-Sep-27
# '''

# import pickle
# import streamlit as st
# import requests
# from streamlit_lottie import st_lottie

# # Function to fetch Lottie animations
# def load_lottieurl(url):
#     try:
#         r = requests.get(url)
#         if r.status_code != 200:
#             return None
#         return r.json()
#     except requests.exceptions.RequestException as e:
#         return None

# # Lottie animation (working link)
# movie_lottie = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_cbrbre30.json")

# # Fetch movie poster
# def fetch_poster(movie_id):
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
#     data = requests.get(url).json()
#     poster_path = data['poster_path']
#     full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
#     return full_path

# # Recommend movies based on similarity
# def recommend(movie):
#     index = movies[movies['title'] == movie].index[0]
#     distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
#     recommended_movie_names = []
#     recommended_movie_posters = []
#     for i in distances[1:6]:
#         movie_id = movies.iloc[i[0]].movie_id
#         recommended_movie_posters.append(fetch_poster(movie_id))
#         recommended_movie_names.append(movies.iloc[i[0]].title)
#     return recommended_movie_names, recommended_movie_posters

# # Set a more stylish header with animations
# st.markdown("<h1 style='text-align: center; color: #FF6347; font-family: Arial Black;'>🍿 Movie Recommender System 🎬</h1>", unsafe_allow_html=True)

# # Only render the Lottie animation if it loads successfully
# if movie_lottie:
#     st_lottie(movie_lottie, speed=1, height=200, key="movie_lottie")

# # Load movie data
# movies = pickle.load(open('artifacts/movie_list.pkl','rb'))
# similarity = pickle.load(open('artifacts/similarity.pkl','rb'))

# movie_list = movies['title'].values
# selected_movie = st.selectbox(
#     "🎥 Select a movie to get recommendations:", movie_list, index=0, help="Choose a movie from the dropdown"
# )

# # Display recommendations when the button is clicked
# if st.button('🎯 Show Recommendations'):
#     recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

#     st.markdown("<h3 style='text-align: center; color: #32CD32;'>✨ Movies you might love ✨</h3>", unsafe_allow_html=True)
    
#     # Use grid layout to show movie posters and names with a modern look
#     cols = st.columns(5)
#     for i, col in enumerate(cols):
#         with col:
#             st.image(recommended_movie_posters[i], use_column_width=True)
#             st.markdown(f"<h4 style='text-align: center; color: #4682B4;'>{recommended_movie_names[i]}</h4>", unsafe_allow_html=True)

# # Add a cool footer for professional touch
# st.markdown(
#     """
#     <style>
#     footer {
#         visibility: hidden;
#     }
#     .css-1q8dd3e {
#         background-color: #2c3e50;
#         color: white;
#         text-align: center;
#         padding: 1rem;
#     }
#     </style>
#     <footer class="css-1q8dd3e">
#     Developed with ❤️ by a pro coder | 2024
#     </footer>
#     """, unsafe_allow_html=True
# )


'''
Author: Shivaya Pandey
Email: pandeyshivaya@gmail.com
Date: 2024-Sep-27
'''

import pickle
import streamlit as st
import requests
from streamlit_lottie import st_lottie
import json

# Function to fetch Lottie animations
def load_lottieurl(url):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except requests.exceptions.RequestException as e:
        return None

# Lottie animation (working link)
movie_lottie = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_cbrbre30.json")

# Fetch movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path

# Recommend movies based on similarity
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# Function to construct the detailed prompt
def construct_prompt(user_input):
    rules = """
    You are a highly knowledgeable movie recommendation assistant. Follow these rules:
    1. Provide movie recommendations based on the user's input.
    2. Ensure the recommendations are relevant and popular.
    3. If the user asks for a specific genre, include movies from that genre.
    4. If the user asks for movies similar to a specific movie, provide similar movies.
    5. Be polite and professional in your responses.
    6. STRICTLY ONLY PROVIDE MOVIE NAMES NOTHING ELSE BUT PROPERLY AND IN POINTS
    """
    prompt = f"{rules}\n\nUser input: {user_input}\n\nRecommendations:"
    return prompt

# Function to get response from TuneStudio API
def get_tune_response(prompt):
    url = "https://proxy.tune.app/chat/completions"
    headers = {
        "Authorization": "nbx_VeHD2srWIz956BM6ocYEIA2sVapnvoTboFg",
        "Content-Type": "application/json",
    }
    data = {
        "temperature": 0.9,
        "messages": [
            {"role": "system", "content": "You are TuneStudio"},
            {"role": "user", "content": prompt}
        ],
        "model": "meta/llama-3.1-70b-instruct",
        "stream": False,
        "frequency_penalty": 0.2,
        "max_tokens": 100
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Function to extract and format the response content
def extract_response_content(response):
    try:
        content = response['choices'][0]['message']['content']
        return content
    except (KeyError, IndexError):
        return "Sorry, I couldn't process the response."

# Set a more stylish header with animations
st.markdown("<h1 style='text-align: center; color: #FF6347; font-family: Arial Black;'>🍿 Movie Recommender System 🎬</h1>", unsafe_allow_html=True)

# Only render the Lottie animation if it loads successfully
if movie_lottie:
    st_lottie(movie_lottie, speed=1, height=200, key="movie_lottie")

# Load movie data
movies = pickle.load(open('artifacts/movie_list.pkl','rb'))
similarity = pickle.load(open('artifacts/similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "🎥 Select a movie to get recommendations:", movie_list, index=0, help="Choose a movie from the dropdown"
)

# Display recommendations when the button is clicked
if st.button('🎯 Show Recommendations'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    st.markdown("<h3 style='text-align: center; color: #32CD32;'>✨ Movies you might love ✨</h3>", unsafe_allow_html=True)
    
    # Use grid layout to show movie posters and names with a modern look
    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.image(recommended_movie_posters[i], use_column_width=True)
            st.markdown(f"<h4 style='text-align: center; color: #4682B4;'>{recommended_movie_names[i]}</h4>", unsafe_allow_html=True)

# Add a section for natural language queries
st.markdown("<h2 style='text-align: center; color: #FF6347;'>💬 Ask for Movie Recommendations</h2>", unsafe_allow_html=True)
user_input = st.text_input("Ask for movie recommendations in natural language:")
if st.button("Get Recommendations"):
    if user_input:
        prompt = construct_prompt(user_input)
        response = get_tune_response(prompt)
        content = extract_response_content(response)
        st.write(content)
    else:
        st.error("Please enter a request.")

# Add a cool footer for professional touch
st.markdown(
    """
    <style>
    footer {
        visibility: hidden;
    }
    .css-1q8dd3e {
        background-color: #2c3e50;
        color: white;
        text-align: center;
        padding: 1rem;
    }
    </style>
    <footer class="css-1q8dd3e">
    Developed with ❤️ by a pro coder | 2024
    </footer>
    """, unsafe_allow_html=True
)