from django.db import models
from django import forms

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

# Methods of payment available
class Payment_method(models.Model):
        method = models.CharField(primary_key=True,max_length=50)

class Transation(models.Model):
    transationID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    # Deposit or withdraw
    type = models.CharField(max_length=50,null=False)
    # Method of payment
    method = models.ForeignKey(Payment_method,on_delete=models.CASCADE)
    # Transation amount
    amount = models.FloatField()
    # Date and time of the operation
    datetime = models.DateTimeField(auto_now_add=True)
