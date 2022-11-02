from django.shortcuts import render
from accounts.models import User,Session
from game.models import load_ucras,Game,Odd,Odd_type
import requests

# Create your views here.
def home(request):
    #load ucras api to database
    load_ucras('http://ucras.di.uminho.pt/v1/games/')
    cookie = request.COOKIES.get("session")
    # get all games
    games = Game.objects.all().values()
    print(games)
    main_listing = []
    # Group each game with the odds in a dictionary
    for g in games:
        odds = Odd.objects.filter(game_id=g['game_id'])
        game_dict = {}
        game_dict["game"] = g
        for odd_obj in odds:
            type =  getattr(odd_obj, "odd_type")
            odd = getattr(odd_obj, "odd")
            if type.str() == "home":
                game_dict["home_odd"] = odd
            elif type.str() == "away":
                game_dict["away_odd"] = odd
            elif type.str() == "draw":
                game_dict["draw_odd"] = odd
        main_listing.append(game_dict)


    print(main_listing)
    if cookie:
        session = Session.objects.get(session_id=cookie)
        context = {

                "logged" : True,
                "id" : session.user_in_session.userID,
                "fname" : session.user_in_session.first_name,
                "balance" : session.user_in_session.balance,
                "games_info" : main_listing,
        }
    else:
        context = {
                "logged" : False,
                "games_info" : main_listing
            }

    return render(request, 'index.html',context)
