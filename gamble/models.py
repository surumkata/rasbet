from django.db import models
from game.models import *
from accounts.models import *

# Types of bets
class Bet_type(models.Model):
    type = models.CharField(primary_key=True,max_length=50)

    def __str__(self):
        return self.type

    def str(self):
        return  self.type


class Bet_status(models.Model):
    status = models.CharField(primary_key=True,max_length=10)
    def __str__(self):
        return self.status

    def str(self):
        return  self.status

    class Meta:
        verbose_name_plural = 'Bet_status'


class Bet(models.Model):
    betID = models.AutoField(primary_key=True)
    # Speficy type of bet
    type = models.ForeignKey(Bet_type, on_delete=models.CASCADE)
    # Amount of money
    amount = models.FloatField()
    # Datetime of the bet
    datetime = models.DateField(auto_now_add=True)
    # Status of the bet, open, won or lost
    status = models.ForeignKey(Bet_status, on_delete=models.CASCADE)

    @classmethod
    def create(self,type,amount):
        bet_type = Bet_type.objects.get(type=type)
        status = Bet_status.objects.get(status='open')
        return Bet.objects.create(type=bet_type,amount=amount,status=status)


    # Arguments : Total amount of the bet , Array od dictionaries {game_id,odd_type,amount}
    def place_simple(user_obj,gamesBet):
        # Cada jogo do dicionário é uma simples
        for dict in gamesBet:
            bet_obj = Bet.create(type='simple',amount=float(dict['amount']))
            game_obj = Game.objects.get(game_id=dict['game_id'])
            odd_type_obj = Odd_type.objects.get(type=dict['bet_outcome'])
            odd_obj = Odd.objects.get(game=game_obj,odd_type=odd_type_obj)
            Bet_game.create(bet=bet_obj,odd_id=odd_obj,odd=odd_obj.odd)
            # Add to user History
            History.create(bet=bet_obj,user=user_obj)


    # Arguments : Total amount of the bet , Array od dictionaries {game_id,odd_type}
    def place_multiple(user_obj,total_amount,gamesBet):
        bet_obj = Bet.create(type='multiple',amount=total_amount)
        # Add to user History
        History.create(bet=bet_obj,user=user_obj)
        # Os jogos do dicionário juntos constituem uma múltipla
        for dict in gamesBet:
            game_obj = Game.objects.get(game_id=dict['game_id'])
            odd_type_obj = Odd_type.objects.get(type=dict['bet_outcome'])
            odd_obj = Odd.objects.get(game=game_obj,odd_type=odd_type_obj)
            Bet_game.create(bet=bet_obj,odd_id=odd_obj,odd=odd_obj.odd)

    def turn_won(self):
        status = Bet_status.objects.get(status='won')
        self.status = status
        value = self.total_gains()
        user = History.objects.get(bet=self).user
        Transation.regist(user,'bet_won','balance',value)


    def turn_lost(self):
        status = Bet_status.objects.get(status='lost')
        self.status = status

    #turn its status, if the case, to won or lost
    def check_status(self):
        lost = False
        open = False
        bet_games = Bet_game.objects.filter(bet=self)
        index = 0

        for bet in bet_games:
            if bet.get_status() == 'lost':
                lost = True 
                break
            elif bet.get_status() == 'open':
                open = True

        if lost:
            self.turn_lost() 
        elif not open:
            self.turn_won()
        
            


    #returns the total amount that can be gained (single or multiple bet)
    def total_gains(self):
        bet_games = Bet_game.objects.filter(bet=self)
        odd_value = 0
        for bet in bet_games:
            odd_value += bet.odd
        return odd_value * self.amount




class Bet_game(models.Model):
    bet = models.ForeignKey(Bet, on_delete=models.CASCADE)
    odd_id = models.ForeignKey(Odd, on_delete=models.CASCADE,default="")
    status = models.ForeignKey(Bet_status, on_delete=models.CASCADE)
    odd = models.FloatField()


    @classmethod
    def create(self,bet,odd_id,odd):
        status = Bet_status.objects.get(status='open')
        Bet_game.objects.create(bet=bet,odd_id=odd_id,odd=odd,status=status)

    def turn_won(self):
        status = Bet_status.objects.get(status='won')
        self.status = status

    def turn_lost(self):
        status = Bet_status.objects.get(status='lost')
        self.status = status

    def get_status(self):
        return str(Bet_status.objects.get(status=self.status))
