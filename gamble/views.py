from django.shortcuts import render,redirect
from .models import *
from game.models import *
from accounts.models import Session,History
from django.http.response import JsonResponse
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
                    #History.create(session.user_in_session,)
            else:
                if session.user_in_session.withdraw_bet(float(slip['amount'])):
                    session.user_in_session.save()
                    Bet.place_multiple(session.user_in_session,float(slip['amount']),slip['games'])

        return redirect('/')
