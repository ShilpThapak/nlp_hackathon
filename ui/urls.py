
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('sentiment_analysis', views.sentiment_analysis, name="sentiment_analysis"),
    path('emotional_traits', views.emotional_traits, name="emotional_traits")
]