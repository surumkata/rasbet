from django.db import models
from django import forms

# Create your models here.
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
        if not User.objects.filter(email=email).exists():
            User.objects.create(first_name=first_name,last_name=last_name,email=email,birthday=birthday,password=password)


    @classmethod
    def verify_login(self,email,password):
        if User.objects.filter(email=email,password=password).exists():
            return True
        else: return False

        ## returnar um booleanprin


class Transations(models.Model):
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    # Type of transation
    wasDeposit = models.BooleanField()
    wasWithdraw = models.BooleanField()
    # Method of payment
    wasMbway = models.BooleanField()
    wasCard = models.BooleanField()
    # Amount of the oporation
    amount = models.FloatField()
    # Date and time of the operation
    datetime = models.DateTimeField()
