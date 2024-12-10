from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recommend/', views.recommend, name='recommend'),
    path('movie-suggestions', views.movie_suggestions, name='movie_suggestions'),
]