from django.http import JsonResponse
from django.shortcuts import render

from django.shortcuts import render
from .recommendations_model import recommend_movie, movies


def home(request):
    return render(request, 'recommendation_system/home.html')


def recommend(request):
    searched_movie_name = request.GET.get('movie', '').strip()
    if searched_movie_name:
        recommended_movies = recommend_movie(searched_movie_name)
        return JsonResponse(recommended_movies)
    else:
        return JsonResponse({"Movie name is empty"})
    return render(request, 'recommendation_system/home.html')

def movie_suggestions(request):
    query = request.GET.get('query', '').strip().lower()
    if query:
        suggestions = movies[movies['Title'].str.lower().str.startswith(query)]['Title'].tolist()
        return JsonResponse({'suggestions': suggestions[:10]})  # Return top 10 suggestions
    return JsonResponse({'suggestions': []})

