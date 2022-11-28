from django.shortcuts import render,redirect
from accounts.models import *
from game.models import *
import requests


# Create your views here
def home(request):

    cookie = request.COOKIES.get("session")
    # get all games
    games = Game.objects.all().values()

    main_listing = []
    # Group each game with the odds in a dictionary
    for g in games:
        details = open_game_details(g)
        if details!={}:
            main_listing.append(details)

    sports_listing = sports_list()

    context = {
                    "logged" : False,
                    "games_info" : main_listing,
                    "sports_info" : sports_listing,
                }
    response = render(request, 'index.html',context)
    try:
        if cookie:
            session = Session.objects.get(session_id=cookie)
            context = {
                    "logged" : True,
                    "id" : session.user_in_session.userID,
                    "fname" : session.user_in_session.first_name,
                    "balance" : session.user_in_session.balance,
                    "games_info" : main_listing,
                    "sports_info" : sports_listing,
            }
            response = render(request, 'index.html',context)
            if Admin.is_admin(session.user_in_session.userID):
                context = {
                    "logged" : True,
                    "admin" : True,
                    "id" : session.user_in_session.userID,
                    "fname" : session.user_in_session.first_name,
                    "games_info" : main_listing,
                    "sports_info" : sports_listing,
                }
                response = render(request, 'admin.html',context)
            elif Specialist.is_specialist(session.user_in_session.userID):
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
                    "games_info" : main_listing,
                    "sports_info" : sports_listing,
                }
            response = render(request, 'index.html',context)
            response.delete_cookie('session')
    return response
