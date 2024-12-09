import pandas as pd
from difflib import get_close_matches
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

movies_list = pd.read_csv('/Users/laxmanmadipadige/Downloads/MovieRecommendationSystem/recommendation_system/imdb-movies-dataset.csv')

movies = movies_list.drop(['Metascore', 'Certificate'], axis=1)
movies.dropna(inplace=True)

# movies = movies[['Poster', 'Title', 'Genre', 'Director', 'Cast', 'Description', 'Rating']]
movies['Genre'] = movies['Genre'].apply(lambda x: x.replace(',', ' '))
movies['Cast'] = movies['Cast'].apply(
    lambda x: ' '.join([item.replace(' ', '') for item in x.split(',')])
)
movies['Director'] = movies['Director'].apply(lambda x: x.replace(' ', ''))
movies = movies.reset_index(drop=True)


def compute_similarity(col):
    cv = TfidfVectorizer(ngram_range=(1, 3), analyzer='char', stop_words='english')
    vectors = cv.fit_transform(movies[col]).toarray()
    sim = cosine_similarity(vectors)
    return sim


sim_genre = compute_similarity('Genre')
sim_dir = compute_similarity('Director')
sim_cast = compute_similarity('Cast')
sim_desc = compute_similarity('Description')

weight_genre = 0.2
weight_dir = 0.3
weight_cast = 0.4
weight_desc = 0.1

sim_final = (weight_genre * sim_genre +
             weight_dir * sim_dir +
             weight_cast * sim_cast +
             weight_desc * sim_desc)


def recommend_movie(movie):
    if movie not in movies['Title'].values:
        matches = get_close_matches(movie, movies['Title'], n=1, cutoff=0.6)
        if matches:
            movie = matches[0]
        else:
            return {"error": f"No match found for '{movie}'"}

    idx = movies[movies['Title'] == movie].index[0]
    recommendations = []

    dist = sim_final[idx]
    m_list = sorted(list(enumerate(dist)), reverse=True, key=lambda x: x[1])[1:11]

    searched_movie_time = movies.loc[idx]['Duration (min)']
    searched_rc = movies.loc[idx]['Review Count']
    searched_rt = movies.loc[idx]['Review Title']
    for i in m_list:
        time = movies.iloc[i[0]]['Duration (min)']
        rc = movies.iloc[i[0]]['Review Count']
        rt = movies.iloc[i[0]]['Review Title']
        recommendations.append({
            "title": movies.iloc[i[0]].Title,
            "genre": movies.iloc[i[0]].Genre,
            "director": movies.iloc[i[0]].Director,
            "cast": movies.iloc[i[0]].Cast,
            "score": round(i[1], 2),
            "poster": movies.iloc[i[0]].Poster,
            "rating": movies.iloc[i[0]].Rating,
            "description": movies.iloc[i[0]].Description,
            "duration": time,
            "rc": rc,
            "rt": rt,
            "review": movies.iloc[i[0]].Review,
            "votes": movies.iloc[i[0]].Votes
        })

    return {
        "searched_movie": {
            "title": movies.loc[idx].Title,
            "genre": movies.loc[idx].Genre,
            "director": movies.loc[idx].Director,
            "cast": movies.loc[idx].Cast,
            "poster": movies.loc[idx].Poster,
            "rating": movies.loc[idx].Rating,
            "description": movies.loc[idx].Description,
            "duration": searched_movie_time,
            "src": searched_rc,
            "srt": searched_rt,
            "searched_review": movies.loc[idx].Review,
            "s_votes": movies.loc[idx].Votes
        },
        "recommendations": recommendations
    }


# Example usage
if __name__ == "__main__":
    movie_name = input("Enter a movie name: ")
    result = recommend_movie(movie_name)

    if "error" in result:
        print(result["error"])
    else:
        searched = result["searched_movie"]
        print("\nSearched Movie:")
        print(f"Title: {searched['title']}")
        print(f"Genre: {searched['genre']}")
        print(f"Director: {searched['director']}")
        print(f"Cast: {searched['cast']}\n")

        print("Recommendations:")
        for rec in result["recommendations"]:
            print(f"Title: {rec['title']}")
            print(f"Genre: {rec['genre']}")
            print(f"Director: {rec['director']}")
            print(f"Cast: {rec['cast']}")
            print(f"Score: {rec['score']}\n")
