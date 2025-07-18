import streamlit as st
from recommender import MovieRecommender
from streamlit_lottie import st_lottie
import requests
import json

TMDB_API_KEY = '44aa3c3a355c1689188f531afce66e90'


@st.cache_resource
def load_recommender():
    return MovieRecommender('dataset/movies.csv', TMDB_API_KEY)


st.markdown("""
    <style>
    .block-container {
        padding-top: 0rem;   
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    .title {
        text-align: center;
        font-size: 2.8em;
        font-weight: bold;
        margin-top: 1em;
    }
    .subtitle {
        text-align: center;
        font-size: 1.2em;
        margin-bottom: 2em;
        color: #BBBBBB;
    }
    .input-container {
        display: flex;
        justify-content: center;
        margin-bottom: 1.5em;
    }
    .stTextInput>div>div>input {
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)


st.markdown("""
    <style>
    div.stButton > button {
        background-color: #ff4b4b;
        color: white;
        padding: 0.6em 1.2em;
        font-size: 1em;
        border-radius: 8px;
        border: none;
        transition: background 0.3s ease;
    }
    div.stButton > button:hover {
        background-color: #ff1e1e;
    }
    </style>
""", unsafe_allow_html=True)


# Load the local Lottie animation
def load_lottie_file(filepath):
    with open(filepath, "r") as f:
        return json.load(f)


lottie_animation = load_lottie_file(
    "D:\\Muntaha\\ML\\MatchOrPass\\images\\clapboard.json")

# to reduce space between text n the animation
st.markdown(
    """
    <div style='margin-bottom: -1.5em; margin-top: -2em; display: flex; justify-content: center;'>
    """,
    unsafe_allow_html=True
)
st_lottie(lottie_animation, height=300, key="clapper")
st.markdown("</div>", unsafe_allow_html=True)


recommender = load_recommender()

st.markdown("<div class='title'>Match or Pass: Movie Recommender</div>",
            unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Get 5 similar movie recommendations !!</div>",
            unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    movie_title = st.text_input("🎞️ Enter a movie title:")

    if st.button("Find Similar Movies"):
        recs = recommender.recommend(movie_title)
        if recs:
            st.subheader("Recommendations🎥✮⋆˙")
            for rec in recs:
                col1, col2 = st.columns([1, 3])
                with col1:
                    if rec['poster_url']:
                        st.image(rec['poster_url'], width=200)
                    else:
                        st.write("No poster")
                with col2:
                    st.markdown(f"**{rec['title']}**")

            def load_lottie_file(filepath):
                with open(filepath, "r") as f:
                    return json.load(f)

            lottie_tape = load_lottie_file(
                "D:\\Muntaha\\ML\\MatchOrPass\\images\\rollingtape.json")
            st_lottie(lottie_tape, height=100, key="tape")

        else:
            st.warning("Movie not found! Try another title.")
