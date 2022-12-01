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
    path('history_bets/',views.history_bets,{}),
    path('history_transactions/',views.history_transactions,{}),
    path('profile/',views.profile,{}),
    path('change_password/',views.change_password,{}),
    path('promotions/',views.promotions,{})
]



