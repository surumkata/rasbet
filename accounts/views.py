from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.urls import reverse
from .models import *
from game.models import load_ucras,Game




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


def profile(request):
    cookie = request.COOKIES.get("session")
    context = {
                    "logged" : False,
                }
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
                }
            elif Specialist.is_specialist(user_id):
                context = {
                    "logged" : True,
                    "specialist" : True,
                    "id" : user_id,
                    "fname" : session.user_in_session.first_name,
                }
            else:
                histories = []
                if History.objects.filter(user=user_id).exists():
                    histories = History.objects.get(user=user_id)
                print(histories)
                history = {}
                for h in histories:
                    dic = {}
                    bet_id = h.bet
                    if Bet.objects.filter(betID=bet_id).exists():
                        bet = Bet.objects.filter(betID=bet_id).get()
                        dic['bet_id'] = bet.betID
                        dic['type'] = bet.type
                        dic['amount'] = bet.amount
                        dic['total_odd'] = bet.total_odd
                        dic['datetime'] = str(bet.datetime)
                context = {
                    "logged" : True,
                    "id" : user_id,
                    "fname" : session.user_in_session.first_name,
                    "balance" : session.user_in_session.balance,
                    "history" : history,
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