from django.shortcuts import render,redirect
from .models import *
from game.models import *
from accounts.models import Session
import json
# Create your views here.



def bet(request):

    if request.method == "POST":
         is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        request_data = json.load(request)

        cookie = request.COOKIES.get("session")
        if cookie:
            session = Session.objects.get(session_id=cookie)
        if session:

            slip = request_data.get('slip')

            if slip['bet_type']=="simple":
                total_amount = 0
                for games in slip['games']:
                    total_amount += float(games['amount'])

                if session.user_in_session.withdraw_bet(total_amount):
                    session.user_in_session.save()
                    Bet.place_simple(session.user_in_session,slip['games'])
                else:
                    # change context to eplainx error not enougth balance
                    context = {}
            else:
                if session.user_in_session.withdraw_bet(float(slip['amount'])):
                    session.user_in_session.save()
                    Bet.place_multiple(session.user_in_session,float(slip['amount']),slip['games'])

                    #change context to say bet placed with success
                else:
                    # change context to eplainx error not enougth balance
                    context = {}

    # fazer render com context para limpar a slip
    response = redirect("/")
    return response
