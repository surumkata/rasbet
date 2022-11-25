from django.db import models
from django import forms
from django.utils.crypto import get_random_string

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

    def deposit(self,amount):
        self.balance += amount


    def withdraw(self,amount):
        if(amount > 5 and self.has_sufficient_balance(amount)):
            self.balance -= amount
            return True
        else: return False

    def withdraw_bet(self,amount):
        if(self.has_sufficient_balance(amount)):
            self.balance -= amount
            return True
        else: return False

    def has_sufficient_balance(self,amount):
        if(self.balance >= amount): return True
        else: return False


    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def update(self,password,fname,lname,email,birthday):
        if(self.password == password):
            if(self.email != email and User.objects.filter(email=email).exists()):
                return 1
            else:
                self.email = email
                self.first_name = fname
                self.last_name = lname
                self.birthday = birthday
                #self.password = password
                self.save()
                return 0
        else: return 2
    
    def change_password(self,password,new_password):
        if(self.password == password):
            self.password = new_password
            return 0
        else: return 1
            


#Admin module
class Admin(models.Model):
    adminID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)

    @classmethod
    def is_admin(self,id:str):
        return Admin.objects.filter(userID=id).exists()

class Specialist(models.Model):
    specID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)

    @classmethod
    def is_specialist(self,id:str):
        return Specialist.objects.filter(userID=id).exists()

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


    @classmethod
    def get(self,user):
        if Session.exists(user):
            return Session.objects.get(user_in_session=user).session_id
        else:
            return None

    # Close session (delete it from db)
    @classmethod
    def close(self,session_id):
        Session.objects.filter(session_id=session_id).delete()

    # Close all sessions (delete it from db)
    @classmethod
    def close_all(self):
        for o in Session.objects.all():
            o.delete()


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
            pm = Payment_method.objects.get(method=method)
            # Regist of the transation
            Transation.objects.create(user=user,type=type,method=pm,amount=amount)
            # Updates user balance
            if type=="deposit":
                user.deposit(float(amount))
            elif type=="withdraw":
                user.withdraw(float(amount))
            user.save()
            return True

        return False


        # fazer transaiton DEPOSIT
        # transation withdraw

# Users betting history
class History(models.Model):
    # Compose key betID+userID, history mapss all bets from all users
    bet  = models.ForeignKey("gamble.Bet",on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name = "history")
    unique_together = ((bet,user))

    @classmethod
    def create(self,bet,user):
        History.objects.create(bet=bet,user=user)