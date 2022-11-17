from django.urls import path
from . import views


urlpatterns = [
    path('login/',views.login,{}),
    path('logout/',views.logout,{}),
    path('signup/',views.signup,{}),
    path('balance/',views.balance,{}),
    path('deposit/',views.deposit,{}),
    path('deposit/mbway/',views.mbway,{}),
    path('withdraw/',views.withdraw,{}),
    path('my-bets/',views.history,{}),
    path('profile/',views.profile,{}),
]
