from django.db import models
from game.models import Odd


# Types of bets
class Bet_type(models.Model):
    type = models.CharField(primary_key=True,max_length=50)


class Bet(models.Model):
    betID = models.AutoField(primary_key=True)
    # Speficy type of bet
    type = models.ForeignKey(Bet_type, on_delete=models.CASCADE)
    # Amount of money
    amount = models.FloatField()
    # Total odd of the bet
    total_odd = models.FloatField()
    # Datetime of the bet
    datetime = models.DateField(auto_now_add=True)


class Bet_game(models.Model):
    bet = models.ForeignKey(Bet, on_delete=models.CASCADE)
    odd = models.ForeignKey(Odd, on_delete=models.CASCADE)
