import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
from django.conf import settings

# Load and preprocess dataset
dataset_path = 'recommendation_system/imdb-movies-dataset.csv'
movies_list = pd.read_csv(dataset_path)

movies = movies_list.drop(['Metascore', 'Certificate'], axis=1)
movies.dropna(inplace=True)

movies['Genre'] = movies['Genre'].apply(lambda x: x.replace(',', ' '))
movies['Cast'] = movies['Cast'].apply(lambda x: ' '.join([item.replace(' ', '') for item in x.split(',')]))
movies['Director'] = movies['Director'].apply(lambda x: x.replace(' ', ''))
movies = movies.reset_index(drop=True)


# Define similarity computation function
def compute_similarity(col):
    cv = TfidfVectorizer(ngram_range=(1, 3), analyzer='char')
    vectors = cv.fit_transform(movies[col]).toarray()
    return cosine_similarity(vectors)


# Compute similarity matrices
sim_genre = compute_similarity('Genre')
sim_dir = compute_similarity('Director')
sim_cast = compute_similarity('Cast')
sim_desc = compute_similarity('Description')

# Combine similarity matrices into a final matrix
weight_genre = 0.2
weight_dir = 0.3
weight_cast = 0.4
weight_desc = 0.1

sim_final = (weight_genre * sim_genre +
             weight_dir * sim_dir +
             weight_cast * sim_cast +
             weight_desc * sim_desc)

with open('recommendation_system/sim_final.pkl', 'wb') as f:
    pickle.dump(sim_final, f)

with open('recommendation_system/movies.pkl', 'wb') as f:
    pickle.dump(movies, f)

print("Similarity matrices and movies data saved to .pkl files.")