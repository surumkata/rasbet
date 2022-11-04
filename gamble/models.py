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
    # Datetime of the bet
    datetime = models.DateField(auto_now_add=True)

    @classmethod
    def create(self,type,amount):
        bet_type = Bet_type.objects.get(type=type)
        return Bet.objects.create(type=bet_type,amount=amount)





class Bet_game(models.Model):
    bet = models.ForeignKey(Bet, on_delete=models.CASCADE)
    odd = models.ForeignKey(Odd, on_delete=models.CASCADE)

    @classmethod
    def create(self,bet,odd):
        Bet_game.objects.create(bet=bet,odd=odd)
