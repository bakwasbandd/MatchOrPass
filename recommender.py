import pandas as pd
import numpy as np
import requests 
from sklearn.feature_extraction.text import TfidfVectorizer   #convert textual data into numerical vals
from sklearn.metrics.pairwise import cosine_similarity         # to measure how similar/diff the movies are (based on their names,overviews!!)

class MovieRecommender:
    def __init__(movies, csv_path, tmdb_api_key):
        movies.df = pd.read_csv(csv_path) 
        movies.df = movies.df.dropna(subset=['overview']) #remove missing overviews
        movies.df['combined'] = (  #merging all
            movies.df['overview'].fillna('') + ' ' +
            movies.df['genres'].fillna('') + ' ' +
            movies.df['keywords'].fillna('')
        )
        movies.tfidf = TfidfVectorizer(stop_words='english')  #ignores articles + common words
        movies.tfidf_matrix = movies.tfidf.fit_transform(movies.df['combined'])
        movies.similarity_matrix = cosine_similarity(movies.tfidf_matrix, movies.tfidf_matrix)
        # similarity_matrix[i][j] shows how similar movie i is to movie j.
        movies.indices = pd.Series(movies.df.index, index=movies.df['title']).drop_duplicates()
        movies.tmdb_api_key = tmdb_api_key

    def recommend(movies, title, top_n=5):
        index = movies.indices.get(title)
        if index is None:
            return [] #mpty list if movie not found

        sim_scores = list(enumerate(movies.similarity_matrix[index])) #similarity scores between the target movie and all others
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:top_n+1]  #skip first bec its probably the entered movie
        movie_indices = [i[0] for i in sim_scores]

        recommendations = []
        for i in movie_indices:
            movie_title = movies.df.iloc[i]['title']
            movie_overview = movies.df.iloc[i]['overview']
            poster_url = movies.get_poster_url(movie_title)
            recommendations.append({
                'title': movie_title,
                'overview': movie_overview,
                'poster_url': poster_url
            })
        return recommendations

    def get_poster_url(movies, movie_title):
        #TMDb for movie_title and return full poster URL.
        search_url = f"https://api.themoviedb.org/3/search/movie"
        params = {
            'api_key': movies.tmdb_api_key,
            'query': movie_title
        }
        response = requests.get(search_url, params=params)
        if response.status_code != 200:
            return ""

        data = response.json()
        results = data.get('results')
        if results:
            poster_path = results[0].get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
        return ""
