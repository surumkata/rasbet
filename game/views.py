from collections import OrderedDict
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from accounts.models import FollowedGames, SendingEmail, favorites_list, follows_list, Session, Specialist, User
from game.models import db_change_gameodd, Game,Odd
from django.urls import reverse
import requests

from main.models import change_url_language
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
                    follows = follows_list(session.user_in_session)
                    context['logged'] = True
                    context['id'] =  session.user_in_session.userID
                    context['fname'] = session.user_in_session.first_name
                    context['balance'] = session.user_in_session.balance
                    context['favorites_info'] = fav_list
                    context['follows'] = follows
                    language = session.language
                    context['language'] = language
                    html = change_url_language('index',language)
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
    cookie = request.COOKIES.get("session")
    session = Session.objects.get(session_id=cookie)
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
    language = session.language
    context['language'] = language
    html = change_url_language('specialist',language)
    response = render(request,html,context)
            

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
                    print("GAME: ")
                    print(game)
                    g = games[game]
                    if 'state' in g.keys():
                        db_change_gamestate(game,g['state'])
                    if 'home' in g.keys():
                        db_change_gameodd(game,g['home'],'home')
                    if 'away' in g.keys():
                        db_change_gameodd(game,g['away'],'away')
                    if 'draw' in g.keys():
                        db_change_gameodd(game,g['draw'],'draw')

                    #mandar email 
                    go = Game.objects.get(game_id=game)
                    game_name = f"{go.home} - {go.away}"
                    odd_type_home = Odd_type.objects.get(type='home')
                    odd_type_draw = Odd_type.objects.get(type='draw')
                    odd_type_away = Odd_type.objects.get(type='away')
                    odd_draw = Odd.objects.get(game=game,odd_type=odd_type_draw)
                    odd_home = Odd.objects.get(game=game,odd_type=odd_type_home) 
                    odd_away = Odd.objects.get(game=game,odd_type=odd_type_away)  
                    template = SendingEmail.write_odds_in_template("game/static/template_oddschanged.html",game_name, str(go.home), str(go.away), odd_home.odd, odd_draw.odd, odd_away.odd)
                    
                    print("A enviar")

                    email = SendingEmail(template, "Odds Changed")
                    users = [(k.user.first_name,k.user.email) for k in FollowedGames.objects.filter(game=game)]
                    print(users)
                    email.send_suspend(users)


    return response
