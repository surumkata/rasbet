from django.db import models
from django import forms
from django.utils.crypto import get_random_string
from gamble.models import Bet

# Default User model
class User(models.Model):
    userID = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=200,null=False)
    password = models.CharField(max_length=10,null=False)
    birthday = models.DateField(null=False)
    first_name = models.CharField(max_length=50,null=False)
    last_name = models.CharField(max_length=50,null=False)
    balance = models.FloatField(default=0)

    @classmethod
    def insert(self,first_name,last_name,email,birthday,password):
        # Verify if email is already in use
        if not User.objects.filter(email=email).exists():
            User.objects.create(first_name=first_name,last_name=last_name,email=email,birthday=birthday,password=password)
            return True # New user created
        return False


    @classmethod
    def verify_login(self,email,password):
        if User.objects.filter(email=email,password=password).exists():
            return True
        else: return False

    @classmethod
    def deposit(self,amount):
        self.balance += amount

    @classmethod
    def withdraw(self,amount):
        self.balance -= amount



class Session(models.Model):
    user_in_session = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateField(auto_now_add=True)
    ip_adress = models.CharField(max_length=15,null=False)
    session_id = models.CharField(max_length=32,null=False)

    # Create a new session instance
    @classmethod
    def create(self,user,request):
        session_key = get_random_string(32,allowed_chars="abcdefghijklmnopqrstuvwxyz0123456789")
        # Just to make sure that the key generated is not already in session
        while Session.objects.filter(session_id=session_key).exists():
            session_key = get_random_string(32,allowed_chars="abcdefghijklmnopqrstuvwxyz0123456789")

        user_ip = request.META.get('HTTP_X_FORWARDED_FOR')
        if user_ip:
            ip = user_ip.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        Session.objects.create(user_in_session=user,ip_adress=ip,session_id=session_key)
        return session_key


    # Verify if user already has session
    @classmethod
    def exists(self,user):
        if Session.objects.filter(user_in_session=user).exists():
            return True
        else:
            return False

    # Close session (delete it from db)
    @classmethod
    def close(self,session_id):
        Session.objects.filter(session_id=session_id).delete()


# Methods of payment available
class Payment_method(models.Model):
        method = models.CharField(primary_key=True,max_length=50)

# Transations (withdraw or deposit) from user
class Transation(models.Model):
    transationID = models.AutoField(primary_key=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Deposit or withdraw
    type = models.CharField(max_length=50,null=False)
    # Method of payment
    method = models.ForeignKey(Payment_method,on_delete=models.CASCADE)
    # Transation amount
    amount = models.FloatField()
    # Date and time of the operation
    datetime = models.DateTimeField(auto_now_add=True)

    @classmethod
    def regist(self,user,type,method,amount):
        if Payment_method.objects.filter(method=method).exists():
            # Regist of the transation
            Session.objects.create(user,type,method,amount)
            # Updates user balance
            if type=="DEPOSIT":
                u.deposit(amount)
            elif type=="WITHDRAW":
                u.withdrae(amount)
            return True
        return False


        # fazer transaiton DEPOSIT
        # transation withdraw

# Users betting history
class History(models.Model):
    # Compose key betID+userID, history mapss all bets from all users
    bet  = models.ForeignKey(Bet,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    unique_together = ((bet,user))
