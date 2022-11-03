from django.urls import path
from . import views

urlpatterns = [
    path('bet/',views.bet,{}),

]
