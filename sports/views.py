from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.utils.decorators import method_decorator
from accounts.models import User,Session
from game.models import load_ucras,Game,Odd
from django.urls import reverse
import requests
from .models import *

#pagina dos desportos
def sports(request):
    print('here')
    cookie = request.COOKIES.get("session")
    
    context = {
                    "logged" : False,
                }
    try:
        if cookie:
            session = Session.objects.get(session_id=cookie)
            context = {

                    "logged" : True,
                    "id" : session.user_in_session.userID,
                    "fname" : session.user_in_session.first_name,
            }
        response = render(request, 'sports.html',context)
    #tratar de quando cookie existe, mas a sessao nao
    except Exception:
        response = render(request, 'sports.html',context)
        if cookie:   
            response.delete_cookie('session') 

    return response
