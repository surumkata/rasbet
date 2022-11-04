from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from accounts.models import User, Session, Admin
from game.models import load_ucras, Game, Odd,db_change_games_state
from django.urls import reverse
import requests
from .models import *

# pagina dos desportos


def sports_page(request):
    sports_listing = sports_list()

    cookie = request.COOKIES.get("session")

    context = {
                    "logged": False,
                    "sports_info": sports_listing,
                }
    try:
        if cookie:
            session = Session.objects.get(session_id=cookie)
            context = {

                    "logged": True,
                    "id": session.user_in_session.userID,
                    "fname": session.user_in_session.first_name,
                    "balance": session.user_in_session.balance,
                    "sports_info": sports_listing,
            }
        response = render(request, 'sports_page.html', context)
    # tratar de quando cookie existe, mas a sessao nao
    except Exception:
        response = render(request, 'sports_page.html', context)
        if cookie:
            response.delete_cookie('session')

    return response


# page to list all bets of a sport
def sport(request):
    if request.method == 'GET':
        sport = request.GET.get('sport')
        if sport:
            games = Game.objects.filter(sport_id=sport).values()
            games_listing = []
            for game in games:
                games_listing.append(game_details(game))
            sports_listing = sports_list()
            cookie = request.COOKIES.get("session")

            context = {
                            "logged": False,
                            "games_info": games_listing,
                            "sports_info": sports_listing,
                        }
            try:
                response = render(request, 'sport.html', context)
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
                    if Admin.is_admin(session.user_in_session.userID):
                        context = {
                            "logged": True,
                            "admin": True,
                            "id": session.user_in_session.userID,
                            "fname": session.user_in_session.first_name,
                            "games_info": games_listing,
                            "sports_info": sports_listing,
                        }
                        response = render(request, 'sport_admin.html', context)
            # tratar de quando cookie existe, mas a sessao nao
            except Exception:
                response = render(request, 'sport.html', context)
                if cookie:
                    response.delete_cookie('session')
        else:
            print('erro')
            response = render(request, 'index.html',)
    else:
        response = redirect('/')
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
                if Admin.is_admin(session.user_in_session.userID):
                    context = {
                        "logged": True,
                        "admin": True,
                        "id": session.user_in_session.userID,
                        "fname": session.user_in_session.first_name,
                        "games_info": games_listing,
                        "sports_info": sports_listing,
                    }
                    response = render(request, 'admin.html', context)
                    games_to_change = []
                    iterate = list(request.GET)
                    iterate.pop(0)
                    #guarda tuplo de jogo e estado para mudar
                    for query in iterate:
                        games_to_change.append((query,request.GET.get(query)))
                    db_change_games_state(games_to_change)
        # tratar de quando cookie existe, mas a sessao nao
        except Exception as e:
            print(e)
            response = render(request, 'index.html',context)
            if cookie:   
                response.delete_cookie('session') 
    else:
        response = redirect('/')
    return response