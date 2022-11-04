from django.shortcuts import render
from accounts.models import User,Session
from game.models import load_ucras,Game,Odd,Odd_type,game_odds
import requests

# Create your views here.
def home(request):
    #load ucras api to database
    #load_ucras('http://ucras.di.uminho.pt/v1/games/')
    cookie = request.COOKIES.get("session")
    # get all games
    games = Game.objects.all().values()
    print(games)
    main_listing = []
    # Group each game with the odds in a dictionary
    for g in games:
        main_listing.append(game_odds(g))


    print(main_listing)


    context = {
                    "logged" : False,
                    "games_info" : main_listing
                }
    try:
        if cookie:
            session = Session.objects.get(session_id=cookie)
            context = {

                    "logged" : True,
                    "id" : session.user_in_session.userID,
                    "fname" : session.user_in_session.first_name,
                    "balance" : session.user_in_session.balance,
                    "games_info" : main_listing,
            }
        response = render(request, 'index.html',context)
        
    except Exception:
        if cookie:
            response = render(request, 'index.html',context)
            response.delete_cookie('session')

    return response
