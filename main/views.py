from django.shortcuts import render,redirect
from accounts.models import *
from game.models import *
import requests
from collections import OrderedDict


# Create your views here
def home(request):

    cookie = request.COOKIES.get("session")
    # get all games
    ordered_by_nb = False

    games = Game.objects.all()
    games = detail_games(games,ordered_by_nb)
    games = OrderedDict(sorted(games.items()))

    # ORDERNAR POR MAIS APOSTADOS main_listing.sort(key=takeNB,reverse=True)

    sports_listing = sports_list()
    print(sports_listing)

    context = {
                    "logged" : False,
                    "games_info" : games,
                    "sports_info" : sports_listing,
                }
    response = render(request, 'index.html',context)
    try:
        if cookie:
            session = Session.objects.get(session_id=cookie)
            user_id = session.user_in_session.userID
            fav_list = favorites_list(session.user_in_session)
            context = {
                    "logged" : True,
                    "id" : session.user_in_session.userID,
                    "fname" : session.user_in_session.first_name,
                    "balance" : session.user_in_session.balance,
                    "games_info" : games,
                    "sports_info" : sports_listing,
                    "favorites_info" : fav_list,
            }
            response = render(request, 'index.html',context)
            if Specialist.is_specialist(user_id):
                on_hold = State.objects.get(state="on_hold")
                open = State.objects.get(state="open")
                games_onhold = Game.objects.filter(state=on_hold).values()
                games_open = Game.objects.filter(state=open).values()
                open_listing = []
                onhold_listing = []
                # Group each game with the odds in a dictionary
                for g in games_open:
                    open_listing.append(game_details(g))
                for g in games_onhold:
                    onhold_listing.append(game_details(g))

                context = {
                    "logged" : True,
                    "specialist" : True,
                    "id" : session.user_in_session.userID,
                    "fname" : session.user_in_session.first_name,
                    "games_open" : open_listing,
                    "games_onhold" : onhold_listing,
                    "sports_info" : sports_listing,
                }
                response = render(request, 'specialist.html',context)

    except Exception as e:
        print(e)
        if cookie:
            context = {
                    "logged" : False,
                    "games_info" : games,
                    "sports_info" : sports_listing,
                }
            response = render(request, 'index.html',context)
            response.delete_cookie('session')
    return response
