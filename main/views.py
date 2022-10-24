from django.shortcuts import render
from accounts.models import User
import requests

# Create your views here.
def home(response):
    #gamesInfo =  requests.get('http://ucras.di.uminho.pt/v1/games/').json()
    #print(gamesInfo)
    if 'logged' in response.session:
        u = User.objects.get(userID = response.session['logged'])
        context = {

                "logged" : True,
                "id" : u.userID,
                "fanme" : u.first_name,
                "balance" : u.balance,
                "session" : response.session['logged'],
        }
    else:
        context = {
                "logged" : False,
            }

    return render(response, 'index.html',context)
