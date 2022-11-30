from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.urls import reverse
from .models import *
from game.models import Game
from gamble.models import Bet_game,Odd,Bet,Bet_status





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
    if session_id:
        u = Session.objects.get(session_id=session_id)
        context = {
            "balance" : u.user_in_session.balance,
            "logged" : True,
            "id" : u.user_in_session.userID,
            "fname" : u.user_in_session.first_name,
            }
        response = render(request,'balance.html',context)
    else:
        response = redirect('/accounts/login/')

    return response

def deposit(request):
    session_id = request.COOKIES.get("session")

    if session_id:
        response = render(request,'deposit.html')

        if request.method == 'POST':
            exists_promotion = True
            amount = request.POST.get('amount',False)
            promo_code = request.POST.get('promo_code',False)
            session_id = request.COOKIES.get("session")

            request.session['amount'] = amount
            request.session['promo_code'] = promo_code
            #Verify promo_code
            if promo_code:
                if not Deposit_Promotion.objects.filter(promo_code=promo_code).exists():
                    exists_promotion = False

            if request.POST.get('mbway',False) and exists_promotion:
                response = redirect('mbway/')
            elif request.POST.get('card',False) and exists_promotion:
                response = redirect('card/')
            else:
                context = {}
                context['promo_error'] = 1
                response = render(request,'deposit.html',context)
    else:
        response = redirect('/accounts/login/')


    return response

def mbway(request):
    session_id = request.COOKIES.get("session")

    if session_id:
        response = render(request,"mbway.html")
        if request.method == 'POST':
            valid_promotion = True
            amount = request.session.get('amount',False)
            promo_code = request.session.get('promo_code',False)
            reward = 0
            if promo_code:
                promotion = Deposit_Promotion.objects.get(promo_code=promo_code)
                user = Session.objects.get(session_id=session_id).user_in_session
                if promotion.valid(user,amount):
                    reward = promotion.reward
                else:
                    valid_promotion = False

            u = Session.objects.get(session_id=session_id)

            if valid_promotion:
                if Transation.regist(u.user_in_session,"deposit","mbway",amount):
                    if reward > 0:
                        Transation.regist(u.user_in_session,f"promo_code:{promo_code}","promotion",reward)
                    response = redirect('/accounts/balance')
            else:
                context = {}
                context['promo_error'] = 2
                response = render(request,'deposit.html',context)
    else:
        response = redirect('/accounts/login/')

    return response

def withdraw(request):
    session_id = request.COOKIES.get("session")

    if session_id:
        response = render(request,"withdraw.html")
        if request.method == 'POST':
            amount = request.POST.get('amount',False)
            u = Session.objects.get(session_id=session_id)
            if Transation.regist(u.user_in_session,"withdraw","mbway",amount):
                response = redirect('/accounts/balance')
    else:
        response = redirect('/accounts/login/')

    return response

def history_transactions(request):
    session_id = request.COOKIES.get("session")
    session = Session.objects.get(session_id=session_id)

    user_transactions_history = Transation.objects.filter(user=session.user_in_session)
    transactions = []

    for transaction in user_transactions_history:
        transactions.append({
            "type": transaction.type,
            "method" : transaction.method.method,
            "amount" : transaction.amount,
            "date" : transaction.datetime 
            })
            
    context = {
        "logged" : True,
        "id" : session.user_in_session.userID,
        "fname" : session.user_in_session.first_name,
        "transactions" : transactions
    }

    response = render(request,"history_transactions.html",context)

    return response

def history_bets(request):
    session_id = request.COOKIES.get("session")

    if session_id:
        u = Session.objects.get(session_id=session_id)

        user_bet_history = History.objects.filter(user=u.user_in_session)

        bets = []
        for entry in user_bet_history:

            if entry.bet.type.str() == "simple":
                bet_game = Bet_game.objects.get(bet=entry.bet)

                bets.append({
                    "type" : entry.bet.type.str(),
                    "amount" : entry.bet.amount,
                    "odd" : bet_game.odd,
                    "home" : bet_game.odd_id.game.home,
                    "away": bet_game.odd_id.game.away,
                    "bet" : bet_game.odd_id.odd_type.type,
                    "status" : entry.bet.status.status,
                    "date" : str(entry.bet.datetime)
                    })
            else:
                bet_games = Bet_game.objects.filter(bet=entry.bet)
                games = []
                for bet_game in bet_games:
                    games.append({
                        "odd" : bet_game.odd,
                        "home" : bet_game.odd_id.game.home,
                        "away": bet_game.odd_id.game.away,
                        "bet" : bet_game.odd_id.odd_type.type,
                        "status" : bet_game.status.status
                        })

                bets.append({
                    "type" : entry.bet.type.str(),
                    "amount" : entry.bet.amount,
                    "odd" : entry.bet.total_odd(),
                    "games" : games,
                    "status" : entry.bet.status.status,
                    "date" : str(entry.bet.datetime)
                    })


        print(bets)
        context = {
        "logged" : True,
        "id" : u.user_in_session.userID,
        "fname" : u.user_in_session.first_name,
        "balance" : u.user_in_session.balance,
        "bets" : bets
        }
        response = render(request,"history_bets.html",context)

    else:
        response = redirect('/accounts/login/')

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



def promotions(request):

    promotions = Promotion.objects.all()
    context = {
                "logged" : False,
                    }
    promotion_list = []
    for promotion in promotions:
        promotion_list.append(promotion.image_path)
        
    context["promotions"] = promotion_list
    response = render(request, 'promotions.html',context)
    return response