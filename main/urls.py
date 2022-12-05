from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,{}),
    path('change_language',views.change_language,{}),

]
