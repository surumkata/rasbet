from django.shortcuts import render,redirect
from accounts.models import User,Session,Admin,Specialist,Transation
from game.models import load_ucras,Game,Odd,Odd_type,game_details,sports_list
import requests

# Create your views here.
def home(request):
    #load ucras api to database
    #load_ucras('http://ucras.di.uminho.pt/v1/games/')
    cookie = request.COOKIES.get("session")
    # get all games
    games = Game.objects.all().values()

    main_listing = []
    # Group each game with the odds in a dictionary
    for g in games:
        main_listing.append(game_details(g))

    sports_listing = sports_list()

    context = {
                    "logged" : False,
                    "games_info" : main_listing,
                    "sports_info" : sports_listing,
                }
    try:
        response = render(request, 'index.html',context)
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
                context = {
                    "logged" : True,
                    "specialist" : True,
                    "id" : session.user_in_session.userID,
                    "fname" : session.user_in_session.first_name,
                    "games_info" : main_listing,
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
