from django.shortcuts import render
from accounts.models import User,Session
from game.models import load_ucras,Game,Odd
import requests

# Create your views here.
def home(request):
    #load ucras api to database
    load_ucras('http://ucras.di.uminho.pt/v1/games/')
    cookie = request.COOKIES.get("session")

    # get all games
    games = Game.objects.all().values()
    odds = Odd.objects.all().values()
    print(odds)
    
    context = {
                    "logged" : False,
                    "games" : games,
                    "odds" : odds
                }
   # try:
    if cookie:
        session = Session.objects.get(session_id=cookie)
        context = {

                "logged" : True,
                "id" : session.user_in_session.userID,
                "fname" : session.user_in_session.first_name,
                "balance" : session.user_in_session.balance,
                "games" : games,
                "odds" : odds
        }
    response = render(request, 'index.html',context)
    ''' #tratar de quando cookie existe, mas a sessao nao
    except Exception:
        response = render(request, 'index.html',context)
        if cookie:   
            response.delete_cookie('session') 
'''
    return response
