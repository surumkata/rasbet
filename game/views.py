from collections import OrderedDict
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from accounts.models import User, Session,Specialist, favorites_list
from game.models import db_change_gameodd, Game,Odd
from django.urls import reverse
import requests
from .models import *
import json

# page to list all bets of a sport
def filter(request):
    if request.method == 'GET':
        sport = request.GET.get('sport')
        competition = request.GET.get('competition')
        participant = request.GET.get('participant')
        order_by_nb = request.GET.get('order_by_nb')
        get = {
                "sport" : sport,
                "competition" : competition,
                "participant" : participant,
                "order" : order_by_nb,
             }
        if sport or competition or participant or order_by_nb:
            if sport: games = Game.objects.filter(sport=sport)
            elif competition: games = Game.objects.filter(competition=competition)
            elif participant: 
                games = Game.objects.filter(home=participant) | Game.objects.filter(away=participant)
            else: games = Game.objects.all()
            order = False
            if(order_by_nb == "true"): order = True
            games_listing = detail_games(games,order)
            games_listing = OrderedDict(sorted(games_listing.items()))
            sports_listing = sports_list()

            cookie = request.COOKIES.get("session")

            context = {
                            "logged": False,
                            "games_info": games_listing,
                            "sports_info": sports_listing,
                            "get" : get
                        }
            try:

                response = render(request, 'index.html', context)
                if cookie:
                    html = 'index.html'
                    session = Session.objects.get(session_id=cookie)
                    fav_list = favorites_list(session.user_in_session)
                    context['logged'] = True
                    context['id'] =  session.user_in_session.userID
                    context['fname'] = session.user_in_session.first_name
                    context['balance'] = session.user_in_session.balance
                    context['favorites_info'] = fav_list

                    response = render(request, html, context)
            # tratar de quando cookie existe, mas a sessao nao
            except Exception as e:
                print(e)
                response = render(request, 'index.html', context)
                if cookie:
                    response.delete_cookie('session')
        else:
            print('erro')
            response = render(request, 'index.html',)
    else:
        response = redirect('/')

    return response


def filter_specialist(request):
    if request.method == 'GET':
        sport = request.GET.get('sport')
        competition = request.GET.get('competition')
        if sport or competition:
            on_hold = State.objects.get(state="on_hold")
            open = State.objects.get(state="open")
            if sport: 
                games_onhold = Game.objects.filter(sport=sport,state=on_hold).values()
                games_open = Game.objects.filter(sport=sport,state=open).values()
            elif competition:
                games_onhold = Game.objects.filter(competition=competition,state=on_hold).values()
                games_open = Game.objects.filter(competition=competition,state=open).values()
            else:
                games_onhold = Game.objects.filter(state=on_hold).values()
                games_open = Game.objects.filter(state=open).values()


            cookie = request.COOKIES.get("session")
            session = Session.objects.get(session_id=cookie)

            open_listing = []
            onhold_listing = []
            # Group each game with the odds in a dictionary
            for g in games_open:
                open_listing.append(game_details(g))
            for g in games_onhold:
                onhold_listing.append(game_details(g))

            sports_listing = sports_list()

            context = {
                "logged" : True,
                "specialist" : True,
                "id" : session.user_in_session.userID,
                "fname" : session.user_in_session.first_name,
                "games_open" : open_listing,
                "games_onhold" : onhold_listing,
                "sports_info": sports_listing,
            }
    response = render(request, 'specialist.html',context)
            

    return response

def change_games_state(request):
    if request.method == 'GET':
        sport = request.GET.get('sport')
        cookie = request.COOKIES.get("session")
        print(sport)

        if sport is None or sport=='null':
            games = Game.objects.all().values()
        else:
            games = Game.objects.filter(sport_id=sport).values()
        games_listing = []
        for game in games:
            games_listing.append(game_details(game))
        sports_listing = sports_list()
        context = {
                    "logged": False,
                    "games_info": games_listing,
                    "sports_info": sports_listing,
                }

        try:
            response = render(request, 'index.html', context)
            if cookie:
                session = Session.objects.get(session_id=cookie)
                context = {

                        "logged": True,
                        "id": session.user_in_session.userID,
                        "fname": session.user_in_session.first_name,
                        "balance": session.user_in_session.balance,
                        "games_info": games_listing,
                        "sports_info": sports_listing,
                        "sport": sport,
                }

        # tratar de quando cookie existe, mas a sessao nao
        except Exception as e:
            print(e)
            response = render(request, 'index.html',context)
            if cookie:
                response.delete_cookie('session')
    else:
        response = redirect('/')
    return response


def specialist_update_games(request):
    response = redirect("/")
    cookie = request.COOKIES.get("session")
    if cookie:
        session = Session.objects.get(session_id=cookie)
        if request.method == "POST":
            is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

            if is_ajax:
                request_data = json.load(request)

                games = request_data.get('games')

                for game in games:
                    g = games[game]
                    if 'state' in g.keys():
                        db_change_gamestate(game,g['state'])
                    if 'home' in g.keys():
                        db_change_gameodd(game,g['home'],'home')
                    if 'away' in g.keys():
                        db_change_gameodd(game,g['away'],'away')
                    if 'draw' in g.keys():
                        db_change_gameodd(game,g['draw'],'draw')
    return response
