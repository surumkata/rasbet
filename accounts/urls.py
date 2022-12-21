from django.urls import path
from . import views


urlpatterns = [
    path('login/',views.login,{}),
    path('logout/',views.logout,{}),
    path('signup/',views.signup,{}),
    path('balance/',views.balance,{}),
    path('deposit/',views.deposit,{}),
    path('deposit/mbway/',views.mbway,{}),
    path('deposit/card/',views.card,{}),
    path('withdraw/',views.withdraw,{}),
    path('history_bets/',views.history_bets,{}),
    path('history_transactions/',views.history_transactions,{}),
    path('followed_games/',views.followed_games,{}),
    path('profile/',views.profile,{}),
    path('change_password/',views.change_password,{}),
    path('promotions/',views.promotions,{}),
    path('favorites/',views.favorites,{}),
    path('update_favorite/',views.update_favorite,{}),
    path('update_follow/',views.update_follow,{})
]
