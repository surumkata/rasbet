from django.urls import path
from . import views


urlpatterns = [
    path('filter/',views.filter,{}),
    path('filter_specialist/',views.filter_specialist,{}),
    path('specialist_update_games/',views.specialist_update_games,{}),
]
