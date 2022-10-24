from django.db import models
from accounts.models import User

# Types of bets
class Bet_type(models.Model):
    type = models.CharField(primary_key=True,max_length=50)


class Bet(models.Model):
    betID = models.AutoField(primary_key=True)
    # Speficy type of bet
    type = models.ForeignKey(Bet_type, on_delete=models.CASCADE)
    ###outcomes..

    # Amount of money
    amount = models.FloatField()
    # Total odd of the bet
    total_odd = models.FloatField()
    # Datetime of the bet
    datetime = models.DateField(auto_now_add=True)


class History(models.Model):
    # Compose key betID+userID, history mapss all bets from all users
    betID  = models.ForeignKey(Bet,on_delete=models.CASCADE)
    userID = models.ForeignKey(User,on_delete=models.CASCADE)
    unique_together = ((betID,userID))
