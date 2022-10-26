from django.db import models

class Sports(models.Model):
    sport = models.CharField(primary_key=True,max_length=50,null=False)
    has_draw = models.BooleanField()
    is_team_sport = models.BooleanField()

# OPEN | SUSPENDED | CLOSED
class State(models.Model):
    state = models.CharField(primary_key=True,max_length=50,null=False)

# HOME | AWAY | DRAW ...
class Odd_type(models.Model):
    type = models.CharField(primary_key=True,max_length=50,null=False)


class Game(models.Model):
    game_id = models.AutoField(primary_key=True)
    # Specify what kind of sport
    sport = models.ForeignKey(Sports, on_delete=models.CASCADE)
    sate = models.ForeignKey(State, on_delete=models.CASCADE)
    home = models.CharField(max_length=50,null=False)
    away = models.CharField(max_length=50,null=False)
    home_score = models.IntegerField()
    away_score = models.IntegerField()
    datetime = models.DateField(auto_now_add=True)

class Odd(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    odd_type = models.ForeignKey(Odd_type, on_delete=models.CASCADE)
    odd = models.FloatField()
    # True odd_type correct
    happened = models.BooleanField()
