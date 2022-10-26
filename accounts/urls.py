from django.urls import path
from . import views


urlpatterns = [
    path('login/',views.login,{}),
    path('logout/',views.logout,{}),
    path('signup/',views.signup,{}),
    path('balance/',views.balance,{}),
    path('deposit/',views.deposit,{}),
    path('withdraw/',views.withdraw,{})
]
