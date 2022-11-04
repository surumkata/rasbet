from django.urls import path
from . import views


urlpatterns = [
    path('sports_page/',views.sports_page,{}),
    path('sport/',views.sport,{}),
    path('change_games_state',views.change_games_state,{}),
    path('change_games_odds',views.change_games_odds,{}),
]
