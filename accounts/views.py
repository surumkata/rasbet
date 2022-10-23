from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from .models import User


# Create your views here.
def login(response):
    if response.method == 'POST':
        email = response.POST.get('email',False)
        psw = response.POST['psw']

        if User.verify_login(email,psw):
            u = User.objects.get(email=email)
            response.session['logged'] = u.userID
            return redirect('/')
        #else:
            #render error page or smth


    return render(response, 'login.html')

def logout(response):
    del response.session['logged']

    return redirect('/')

def signup(response):
    if response.method == 'POST':
        fname = response.POST['fname']
        lname = response.POST['lname']
        email = response.POST['email']
        birthday = response.POST['birthday']
        psw = response.POST['psw']

        User.insert(fname,lname,email,birthday,psw)
    return render(response, 'signup.html')



def deposit(response):
    return render(response, 'deposit.html')



def withdraw(response):
    return render(response, 'withdraw.html')
