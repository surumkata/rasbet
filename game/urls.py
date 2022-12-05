from django.urls import path
from . import views


urlpatterns = [
    path('filter/',views.filter,{}),
    path('filter_specialist/',views.filter_specialist,{}),
    path('change_games_state/',views.change_games_state,{}),
    path('specialist_update_games/',views.specialist_update_games,{}),
]
