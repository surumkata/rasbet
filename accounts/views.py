from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.urls import reverse
from .models import *
from game.models import Game
from gamble.models import Bet_game,Odd,Bet





def login(request):
    if request.method == 'POST':
        email = request.POST.get('email',False)
        psw = request.POST['psw']
        context = {"error" : False}

        if User.verify_login(email,psw):
            u = User.objects.get(email=email)

            #se ja existe reutiliza a sessao
            #(talvez o melhor a fazer seja apagar a antiga e criar uma nova,
            # para n permitir dois dispositivos na mesma conta)
            if  Session.exists(u):
                session_id = Session.get(u)
                response = redirect("/")
                response.set_cookie('session',session_id)
            else:
                session_id = Session.create(u,request)
                response = redirect("/")
                response.set_cookie('session',session_id)
        else:
            context = {"error" : True,"msg" : "User não existe"}
            response = render(request,'login.html',context)
    else:
        context = {"error" : False, "msg" : ""}
        response = render(request,'login.html',context)

    return response

def logout(request):
    session_id = request.COOKIES.get("session")
    response = redirect('/')
    Session.close(session_id)
    response.delete_cookie('session')

    return response

def signup(request):
    context = {"fail" : False}
    response = render(request, 'signup.html',context)

    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        birthday = request.POST['birthday']
        psw = request.POST['psw']

        if not User.insert(fname,lname,email,birthday,psw):
            context = {"fail" : True}
            response = render(request, 'signup.html',context)
        else:
            u = User.objects.get(email=email)
            session_id = Session.create(u,request)
            response = redirect("/")
            response.set_cookie('session',session_id)


    return response


def balance(request):
    session_id = request.COOKIES.get("session")
    u = Session.objects.get(session_id=session_id)
    context = {
        "balance" : u.user_in_session.balance,
        "logged" : True,
        "id" : u.user_in_session.userID,
        "fname" : u.user_in_session.first_name,
    }
    response = render(request,'balance.html',context)

    return response

def deposit(request):
    response = render(request,'deposit.html')
    if request.method == 'POST':
        amount = request.POST.get('amount',False)
        session_id = request.COOKIES.get("session")

        request.session['amount'] = amount

        if request.POST.get('mbway',False):
            response = redirect('mbway/')
        elif request.POST.get('card',False):
            response = redirect('card/')


    return response

def mbway(request):
    response = render(request,"mbway.html")
    if request.method == 'POST':
        amount = request.session.get('amount',False)
        session_id = request.COOKIES.get("session")
        u = Session.objects.get(session_id=session_id)
        if Transation.regist(u.user_in_session,"deposit","mbway",amount):
            response = redirect('/accounts/balance')

    return response

def withdraw(request):
    response = render(request,"withdraw.html")
    if request.method == 'POST':
        amount = request.POST.get('amount',False)
        session_id = request.COOKIES.get("session")
        u = Session.objects.get(session_id=session_id)
        if Transation.regist(u.user_in_session,"withdraw","mbway",amount):
            response = redirect('/accounts/balance')

    return response

def history_transactions(request):
    response = render(request,"index.html")
    return response

def history_bets(request):
    session_id = request.COOKIES.get("session")
    u = Session.objects.get(session_id=session_id)

    user_bet_history = History.objects.filter(user=u.user_in_session)

    openBets = []
    closedBets = []
    for entry in user_bet_history:

        if entry.bet.type.str() == "simple":

            bet_game = Bet_game.objects.get(bet=entry.bet)

            # Verify if is open or closed bet
            if bet_game.odd_id.game.state.__str__()=="open":
                openBets.append({"type" : entry.bet.type.str() ,"amount" : entry.bet.amount ,"odd" : bet_game.odd,"home" : bet_game.odd_id.game.home,"away": bet_game.odd_id.game.away,"bet" : bet_game.odd_id.odd_type})
            else:
                closedBets.append({"type" : entry.bet.type.str() ,"amount" : entry.bet.amount ,"odd" : bet_game.odd,"home" : bet_game.odd_id.game.home,"away": bet_game.odd_id.game.away,"bet" : bet_game.odd_id.odd_type,"happened" : bet_game.odd_id.happened})
        else:

            bet_games = Bet_game.objects.filter(bet=entry.bet)

            gamesList = []
            is_open = False
            happened = True

            # Verify if is open or closed bet, in multi bet one open game is enougth to be a open bet
            for bet_game in bet_games:
                if bet_game.odd_id.game.state.__str__()=="open":
                    print("open")
                    is_open = True

                if not bet_game.odd_id.happened:
                    happened = False

                gamesList.append({"odd" : bet_game.odd,"home" : bet_game.odd_id.game.home,"away": bet_game.odd_id.game.away,"bet" : bet_game.odd_id.odd_type,"happened" : bet_game.odd_id.happened})


            if is_open:
                openBets.append({"type" : entry.bet.type.str() ,"amount" : entry.bet.amount,"games":gamesList})
            else:
                closedBets.append({"type" : entry.bet.type.str() ,"amount" : entry.bet.amount,"happened": happened,"games":gamesList})

#FALTA DATAS

#Openbets é uma lista de dicionários
# aposta simples -> type,amount,odd,home,away,bet
# aposta multipla -> type,amount, game->odd,home,away,bet

#Closedbets é uma lista de dicionários
# aposta simples -> type,amount,odd,home,away,bet,happened
# aposta multipla -> type,amount,happened, game->odd,home,away,bet,happened

    context = {
        "logged" : True,
        "id" : u.user_in_session.userID,
        "fname" : u.user_in_session.first_name,
        "openBets" : openBets,
        "closedBets" : closedBets
    }

    print("openBets: ")
    print(openBets)
    print("closedBets: ")
    print(closedBets)
    response = render(request,"history_bets.html",context)

    return response

def change_password(request):
    cookie = request.COOKIES.get("session")
    context = {
                "logged" : True,
                    }
    msg = -1
    if request.method == 'POST':
        session = Session.objects.get(session_id=cookie)
        user_id = session.user_in_session.userID
        user = User.objects.get(userID=user_id)

        password = request.POST['psw']
        new_password = request.POST['newpsw']
        confirm_password = request.POST['newpsw2']
        result = user.change_password(password,new_password,confirm_password)
        msg = result
        print("OLA")
    try:
        response = redirect('/accounts/profile')
        if cookie and msg != 0:
            session = Session.objects.get(session_id=cookie)
            user_id = session.user_in_session.userID
            if Admin.is_admin(user_id):
                context = {
                    "logged" : True,
                    "admin" : True,
                    "id" : user_id,
                    "fname" : session.user_in_session.first_name,
                    "msg" : msg
                }
            elif Specialist.is_specialist(user_id):
                context = {
                    "logged" : True,
                    "specialist" : True,
                    "id" : user_id,
                    "msg" : msg
                }
            else:
                context = {
                    "logged" : True,
                    "id" : user_id,
                    "msg" : msg
                }
            print("OLA")
            response = render(request, 'change_password.html',context)

    except Exception as e:
        print('error: '+ str(e))
        if cookie:
            context = {
                    "logged" : False,
                }
            response = render(request, 'index.html',context)
            response.delete_cookie('session')
    return response


def profile(request):
    cookie = request.COOKIES.get("session")
    context = {
                "logged" : False,
                    }
    response = render(request, 'profile.html',context)
    msg = -1
    if request.method == 'POST':
        session = Session.objects.get(session_id=cookie)
        user_id = session.user_in_session.userID
        user = User.objects.get(userID=user_id)

        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        birthday = request.POST['birthday']
        password = request.POST['psw']
        print(fname)
        print(lname)
        #psw = request.POST['psw']
        print("OLA")

        msg = user.update(password,fname,lname,email,birthday)

    try:
        response = render(request, 'index.html',context)
        if cookie:
            session = Session.objects.get(session_id=cookie)
            user_id = session.user_in_session.userID
            if Admin.is_admin(user_id):
                context = {
                    "logged" : True,
                    "admin" : True,
                    "id" : user_id,
                    "fname" : session.user_in_session.first_name,
                    "msg" : msg
                }
            elif Specialist.is_specialist(user_id):
                context = {
                    "logged" : True,
                    "specialist" : True,
                    "id" : user_id,
                    "fname" : session.user_in_session.first_name,
                    "msg" : msg
                }
            else:
                user = {
                    "email" : session.user_in_session.email,
                    "birthday" : str(session.user_in_session.birthday),
                    "first_name" : session.user_in_session.first_name,
                    "last_name" : session.user_in_session.last_name,
                }
                context = {
                    "logged" : True,
                    "id" : user_id,
                    "fname" : session.user_in_session.first_name,
                    "balance" : session.user_in_session.balance,
                    "user" : user,
                    "msg" : msg
                }
            response = render(request, 'profile.html',context)
    except Exception as e:
        print('error: '+ str(e))
        if cookie:
            context = {
                    "logged" : False,
                }
            response = render(request, 'index.html',context)
            response.delete_cookie('session')
    return response
