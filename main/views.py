from django.shortcuts import render
from accounts.models import User

# Create your views here.
def home(response):

    if 'logged' in response.session:
        u = User.objects.get(userID = response.session['logged'])
        context = {

                "logged" : True,
                "id" : u.userID,
                "fanme" : u.first_name,
                "balance" : u.balance,
                "session" : response.session['logged'],
        }
    else:
        context = {
                "logged" : False,
            }

    return render(response, 'index.html',context)
