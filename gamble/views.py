from django.shortcuts import render,redirect
from .models import *
from game.models import *
from accounts.models import History,Session
import json
# Create your views here.



def bet(request):

    if request.method == "POST":
         is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        request_data = json.load(request)

        slip = request_data.get('slip')
        print(slip)
        if slip['bet_type']=="simple":
            print("handle simple bets")
        else:
            print("handle multiple bets")

    response = redirect("/")
    return response
