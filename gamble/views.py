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




    # cookie = request.COOKIES.get("session")
    #
    # if cookie:
    #
    #     session = Session.objects.get(session_id=cookie)
    #
    #     slip = request.COOKIES.get("slip")
    #
    #     slip_fields = slip.split("|")
    #     print(slip_fields[1])
    #     session.user_in_session.withdraw(float(slip_fields[1]))
    #     session.user_in_session.save()
    #     bet_obj = Bet.create(slip_fields[0],slip_fields[1])
    #
    #     game_outcome = slip_fields[2].split("/")
    #
    #     game = Game.objects.get(game_id=game_outcome[0])
    #
    #     type = Odd_type.objects.get(type=game_outcome[1])
    #
    #     odd = Odd.objects.get(game=game,odd_type=type)
    #
    #     Bet_game.create(bet_obj,odd)
    #
    #     History.create(bet_obj,session.user_in_session)
    #
