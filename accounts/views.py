from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from .models import User,Session
from django.utils.decorators import method_decorator


#@method_decorator(ensure_csrf_cookie)
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email',False)
        psw = request.POST['psw']
        context = {"error" : False}

        if User.verify_login(email,psw):
            u = User.objects.get(email=email)

            if  Session.exists(u):
                context = {"error" : True,"msg" : "Já se encontra loggado"}
                response = render(request,'login.html',context)
            else:
                session_id = Session.create(u,request)
                if session_id!=-1:
                    response = redirect("/")
                    response.set_cookie('session',session_id)
    else:
        context = {"error" : False, "msg" : ""}
        response = render(request,'login.html',context)

    return response

def logout(request):
    session_key = request.COOKIES.get("session")
    response = redirect('/')
    Session.close(session_key)
    response.delete_cookie('session')

    return response

def signup(request):
    context = {"fail" : False}
    response = render(request, 'login.html',context)

    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        birthday = request.POST['birthday']
        psw = request.POST['psw']

        if not User.insert(fname,lname,email,birthday,psw):
            context = {"fail" : True}
            response = render(request, 'signup.html',context)


    return response



def deposit(request):
    return render(response, 'deposit.html')



def withdraw(request):
    return render(response, 'withdraw.html')
