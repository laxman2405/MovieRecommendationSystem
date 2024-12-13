import pandas as pd
from difflib import get_close_matches
import pickle
import os
from django.conf import settings
import gdown
import boto3

# Lines 13-29 work only on Amazon EC2 server, as the training data is downloaded from Amazon S3 storage.
# To proceed to run this in local, comment out the lines from 13-29 and line 7, and uncomment the lines 33-54.
# Lines 33-54 will load the training data from google drive.
# To train the model, run the training.py file and then proceed to run in local.
bucket_name = "pkl-bucket-mrs"
similarity_list = "sim_final.pkl"
sim_final = "sim_final.pkl"

movies_list = "movies.pkl"
movies_final = "movies.pkl"

s3 = boto3.client("s3")
s3.download_file(bucket_name, similarity_list, sim_final)
s3.download_file(bucket_name, movies_list, movies_final)

# Load precomputed similarity matrices and movies data
with open(sim_final, 'rb') as f:
    sim_final = pickle.load(f)

with open(movies_final, 'rb') as f:
    movies = pickle.load(f)

# Load precomputed similarity matrices and movies data to run in the local
# if(os.path.exists(os.path.join(settings.BASE_DIR, 'recommendation_system/sim_final.pkl'))):
#     print('inside if')
#     with open(os.path.join(settings.BASE_DIR, 'recommendation_system/sim_final.pkl'), 'rb') as f:
#         sim_final = pickle.load(f)
# else:
#     sim_url = 'https://drive.google.com/file/d/1qrSzBRHtQegZgwtyMQMRghHMY2Mdnx_9/view?usp=drive_link'
#     sim_output = os.path.join(settings.BASE_DIR, 'recommendation_system/sim_final.pkl')
#     gdown.download(sim_url, sim_output, quiet=False, fuzzy=True)
#     with open(sim_output, 'rb') as f:
#         sim_final = pickle.load(f)
#
#
# if(os.path.exists(os.path.join(settings.BASE_DIR, 'recommendation_system/movies.pkl'))):
#     print('inside if-movies')
#     with open(os.path.join(settings.BASE_DIR, 'recommendation_system/movies.pkl'), 'rb') as f:
#         movies = pickle.load(f)
# else:
#     movies_url = 'https://drive.google.com/file/d/10s5nyYRfXczh1ULqXDxRbrc55BN9NTXX/view?usp=drive_link'
#     movies_output = os.path.join(settings.BASE_DIR, 'recommendation_system/movies.pkl')
#     gdown.download(movies_url, movies_output, quiet=False, fuzzy=True)
#     with open(movies_output, 'rb') as f:
#         movies = pickle.load(f)

def recommend_movie(movie):
    not_found = False
    if movie not in movies['Title'].values:
        matches = get_close_matches(movie, movies['Title'], n=1, cutoff=0.6)
        if matches:
            movie = matches[0]
            not_found = True
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
            "s_votes": movies.loc[idx].Votes,
            "notFound": not_found
        },
        "recommendations": recommendations
    }