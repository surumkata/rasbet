from django.shortcuts import render
from accounts.models import User,Session
import requests

# Create your views here.
def home(request):
    #gamesInfo =  requests.get('http://ucras.di.uminho.pt/v1/games/').json()
    #print(gamesInfo)
    cookie = request.COOKIES.get("session")
    if cookie:
        session = Session.objects.get(session_id=cookie)
        context = {

                "logged" : True,
                "id" : session.user_in_session.userID,
                "fanme" : session.user_in_session.first_name,
                "balance" : session.user_in_session.balance,
        }
    else:
        context = {
                "logged" : False,
            }

    return render(request, 'index.html',context)
