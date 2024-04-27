from nbformat import write
import streamlit as st
import pandas as pd
import pickle
import numpy as np
import requests

similarity = pickle.load(open("similarity_tfidf.pkl", "rb"))
movie_dict = pickle.load(open("movies_dict.pkl", "rb"))
movies = pd.DataFrame(movie_dict)
st.title("Movie Recommender System")

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=&language=en-US')

    data = response.json()
    return 'http://image.tmdb.org/t/p/w500/'+data['poster_path']

def recommend_tfidf(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distance_vector = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance_vector)), reverse=True, key=lambda x:x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_poster = []
    for movie in movies_list:
        recommended_movies.append(movies.iloc[movie[0]].title)
        recommended_movies_poster.append(fetch_poster(movies.iloc[movie[0]].movie_id))
        # print(movie_df.iloc[movie[0]].title)

    print(recommended_movies)
    
    return recommended_movies, recommended_movies_poster

def recommend_by_genre(genres_to_filter, c):
    # Filter the DataFrame
    filtered_df = movies[movies['genres_new'].apply(lambda x: all(genre in x for genre in genres_to_filter))]
    
    
    # If the filtered DataFrame has less than 'count' movies, return them all

    if len(filtered_df) < c:
        return filtered_df
    
    # Otherwise, return a random sample of 'count' movies
    filtered_df = filtered_df.sample(n=c, random_state=np.random.RandomState())
    titles = list(filtered_df['title'])
    ids = list(filtered_df['movie_id'])
    recommended_movies_poster = []

    for i in ids:
        try:
            recommended_movies_poster.append(fetch_poster(i))
        except:
            st.write("Not found")

    print(titles, recommended_movies_poster)

    return titles, recommended_movies_poster
    count=0
    recommended_movies_by_genre = []
    recommended_movies_poster = []
    for i, j, k in zip(movies['genres'], movies['title'], movies['movie_id']):
        if genre in i:
            recommended_movies_by_genre.append(j)
            try:
                recommended_movies_poster.append(fetch_poster(k))
            except:
                st.write("Not found")
            count+=1
        if count==c:
            break
    
    if recommended_movies_by_genre==[] or recommended_movies_poster==[]:
        return [], []
    
    print(recommended_movies_by_genre)
    
    return recommended_movies_by_genre, recommended_movies_poster

movie_name = st.selectbox(
    'Select a movie',
    movies['title'].values
)

if st.button('Recommend based on movie name'):
    recommendations, poster = recommend_tfidf(movie_name)
    
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommendations[0])
        st.image(poster[0])

    with col2:
        st.text(recommendations[1])
        st.image(poster[1])

    with col3:
        st.text(recommendations[2])
        st.image(poster[2])
    
    with col4:
        st.text(recommendations[3])
        st.image(poster[3])
    
    with col5:
        st.text(recommendations[4])
        st.image(poster[4])

# genre = st.selectbox(
#     'Select a genre',
#     ['','Action','Adventure','Animation','Comedy','Crime','Documentary','Drama','Family','Fantasy','Foreign', 'History','Horror','Music','Mystery','Romance','ScienceFiction','TVMovie','Thriller','War','Western']
# )
st.subheader("Available Genres")

genre_op = ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy', 'Foreign', ' History', 'Horror', 'Music', 'Mystery', 'Romance', 'ScienceFiction', 'TVMovie', 'Thriller', 'War', 'Western']
# genres = st.text_input('Select genre')
new_genres = st.multiselect("Select genres", genre_op)
lowercase_func = lambda word: word.lower()
new_genres = list(map(lowercase_func, new_genres))

if st.button('Recommend based on genre'):
    # user_genres = new_genres.lower()
    # user_genres = st.multiselect("Select genres", genre_op)
    # print(user_genres)
    print(new_genres)
    recommendations, poster = recommend_by_genre(new_genres, 5)
    
    if len(poster)==0 and len(recommendations)!=0:
        for recommendation in recommendations:
            st.write(recommendation)

    elif recommendations==[] and poster==[]:
        st.write("Not found")

    else:
        #col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            try:
                st.text(recommendations[0])
                st.image(poster[0])
            except:
                st.text("Not found")   

        with col2:
            try:
                st.text(recommendations[1])
                st.image(poster[1])
            except:
                st.text(" ")
        with col3:
            try:
                st.text(recommendations[2])
                st.image(poster[2])
            except:
                st.text(" ")
        with col4:
            try:
                st.text(recommendations[3])
                st.image(poster[3])
            except:
                st.text(" ")
        with col5:
            try:
                st.text(recommendations[4])
                st.image(poster[4])
            except:
                st.text(" ")
        # with col6:
        #     st.text(recommendations[5])
        #     st.image(poster[5])

        # with col7:
        #     st.text(recommendations[6])
        #     st.image(poster[6])

        # with col8:
        #     st.text(recommendations[7])
        #     st.image(poster[7])
        
        # with col9:
        #     st.text(recommendations[8])
        #     st.image(poster[8])
        
        # with col10:
        #     st.text(recommendations[9])
        #     st.image(poster[9])

