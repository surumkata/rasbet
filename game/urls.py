from django.urls import path
from . import views


urlpatterns = [
    path('sports_page/',views.sports_page,{}),
]
