from django.shortcuts import render,redirect
from .models import *
from game.models import *
from accounts.models import Session,History
from django.http import HttpResponse
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
                    for game in slip['games']:
                        total_amount += game['amount']

                    if session.user_in_session.has_sufficient_balance(total_amount):
                        for game in slip['games']:
                            if Transation.regist(session.user_in_session,"bet","balance",game['amount']):
                                Bet.place_simple(session.user_in_session,game)
                                user = session.user_in_session
                                user.update_follow(game["game_id"],True)
                                
                                response = {'status': 0, 'message': "bet placed"}
                    else:
                        response = {'status': 2, 'message': "Not enough balance"}


                else:
                    if Transation.regist(session.user_in_session,"bet","balance",float(slip['amount'])):
                        Bet.place_multiple(session.user_in_session,float(slip['amount']),slip['games'])
                        for game in slip['games']:
                            user = session.user_in_session
                            user.update_follow(game["game_id"],True)
                        response = {'status': 0, 'message': "bet placed"}
                    else:
                        response = {'status': 2, 'message': "Not enough balance"}

            else:
                response = {'status': 1, 'message': "Session expired"}
        else:
            response = {'status': 1, 'message': "Not logged in"}

    print(response)
    return HttpResponse(json.dumps(response), content_type='application/json')
