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

    # Arguments : Total amount of the bet , Array od dictionaries {game_id,odd_type,amount}
    def place_simple(gamesBet):
        bet_type = Bet_type.objects.get(type="simple")

        # Cada jogo do dicionário é uma simples
        for dict in gamesBet:
            bet_obj = Bet.objects.create(type=bet_type,dict['amount'])
            game_obj = Game.objects.get(game_id=dict['game_id'])
            odd_type_obj = Odd_type.objects.get(type=dict['bet_outcome'])
            odd_obj = Odd.objects.get(game=game_obj,odd_type=odd_type_obj)
            Bet_game.create(bet=bet_obj,odd=odd_obj)


    # Arguments : Total amount of the bet , Array od dictionaries {game_id,odd_type}
    def place_multiple(total_amount,gamesBet):
        bet_type = Bet_type.objects.get(type="multiple")
        bet_obj = Bet.objects.create(type=bet_type,amount=total_amount)

        # Os jogos do dicionário juntos constituem uma múltipla
        for dict in gamesBet:
            game_obj = Game.objects.get(game_id=dict['game_id'])
            odd_type_obj = Odd_type.objects.get(type=dict['bet_outcome'])
            odd_obj = Odd.objects.get(game=game_obj,odd_type=odd_type_obj)
            Bet_game.create(bet=bet_obj,odd=odd_obj)



class Bet_game(models.Model):
    bet = models.ForeignKey(Bet, on_delete=models.CASCADE)
    odd_id = models.ForeignKey(Odd, on_delete=models.CASCADE,default="")
    odd = models.FloatField()


    @classmethod
    def create(self,bet,odd):
        Bet_game.objects.create(bet=bet,odd=odd)
