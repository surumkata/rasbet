from django.shortcuts import render,redirect
from .models import *
from game.models import *
from accounts.models import History,Session
# Create your views here.



def bet(request):
    #simple|10|538136a794711c8c9bc24b48353c396c/home
    # if request.method == 'POST':
    #     print("dentro")
    #     print(request.POST['test'])
    cookie = request.COOKIES.get("session")

    session = Session.objects.get(session_id=cookie)

    slip = request.COOKIES.get("slip")

    slip_fields = slip.split("|")
    print(slip_fields[1])
    session.user_in_session.withdraw(float(slip_fields[1]))
    session.user_in_session.save()
    bet_obj = Bet.create(slip_fields[0],slip_fields[1])

    game_outcome = slip_fields[2].split("/")

    game = Game.objects.get(game_id=game_outcome[0])

    type = Odd_type.objects.get(type=game_outcome[1])

    odd = Odd.objects.get(game=game,odd_type=type)

    Bet_game.create(bet_obj,odd)

    History.create(bet_obj,session.user_in_session)



    response = redirect("/")
    return response
