from django.db import models
import requests
from datetime import datetime

class Sport(models.Model):
    sport = models.CharField(primary_key=True,max_length=50,null=False)
    has_draw = models.BooleanField()
    is_team_sport = models.BooleanField()

    def str(self):
        return self.sport


# open | suspended | closed
class State(models.Model):
    state = models.CharField(primary_key=True,max_length=50,null=False)

# home | away | draw ...
class Odd_type(models.Model):
    type = models.CharField(primary_key=True,max_length=50,null=False)

    def str(self):
        return self.type


class Game(models.Model):
    game_id = models.CharField(max_length=50,primary_key=True)
    # Specify what kind of sport
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    sate = models.ForeignKey(State, on_delete=models.CASCADE)
    home = models.CharField(max_length=50,null=False)
    away = models.CharField(max_length=50,null=False)
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)
    datetime = models.DateTimeField()

    def home_scored(self,points):
        self.home_score += points

    def away_scored(self,points):
        self.away_score += points

    # Bets are possible
    def open(self):
        state = State.objects.get(sate="open")
        self.state = state

    # Games has not staarted yet,bets not possible
    def close(self):
        state = State.objects.get(sate="closed")
        self.state = state

    # Games is suspended, bets not possible
    def suspend(self):
        state = State.objects.get(sate="suspended")
        self.state = state

    # Game finished , bets not possible
    def finish(self):
        state = State.objects.get(sate="finish")
        self.state = state

        

    @classmethod
    # Create a game in the database
    def create(self,id,sport,home,away,datetime):
        # The sport MUST exist in the db
        if Sport.objects.filter(sport=sport).exists():
            sport = Sport.objects.get(sport=sport)
            # By default the game state is closed
            state = State.objects.get(state="closed")
            Game.objects.create(game_id=id,sport=sport,sate=state,home=home,away=away,datetime=datetime)




class Odd(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    odd_type = models.ForeignKey(Odd_type, on_delete=models.CASCADE)
    odd = models.FloatField()
    happened = models.BooleanField(default=False)

    @classmethod
    # Create odd to the outcome home team wins
    def home(self,game,odd):
        type = Odd_type.objects.get(type="home")
        Odd.objects.create(game=game,odd_type=type,odd=odd)

    @classmethod
    # Create odd to the outcome away team wins
    def away(self,game,odd):
        type = Odd_type.objects.get(type="away")
        Odd.objects.create(game=game,odd_type=type,odd=odd)

    @classmethod
    # Create odd to the outcome draw
    def draw(self,game,odd):
        type = Odd_type.objects.get(type="draw")
        Odd.objects.create(game=game,odd_type=type,odd=odd)


# Load ucras api data to databse
def load_ucras(url):
    games = requests.get('http://ucras.di.uminho.pt/v1/games/').json()

    for g in games:
        # Only new games are added
        if not Game.objects.filter(game_id=g['id']).exists():
            now = datetime.now().replace(second= 0, microsecond= 0)
            game_date_obj = datetime.strptime(g['commenceTime'][:-8],"%Y-%m-%dT%H:%M")

            # Only upcoming games are added
            if game_date_obj>now:
                Game.create(g['id'],"football",g['homeTeam'],g['awayTeam'],game_date_obj)
                game = Game.objects.get(game_id=g['id'])
                Odd.home(game,g['bookmakers'][1]['markets'][0]['outcomes'][0]['price'])
                Odd.away(game,g['bookmakers'][1]['markets'][0]['outcomes'][1]['price'])
                Odd.draw(game,g['bookmakers'][1]['markets'][0]['outcomes'][2]['price'])


def game_odds(game:dict):
    odds = Odd.objects.filter(game_id=game['game_id'])
    game_dict = {}
    game_dict["game"] = game
    for odd_obj in odds:
        type =  getattr(odd_obj, "odd_type")
        odd = getattr(odd_obj, "odd")
        if type.str() == "home":
            game_dict["home_odd"] = odd
        elif type.str() == "away":
            game_dict["away_odd"] = odd
        elif type.str() == "draw":
            game_dict["draw_odd"] = odd
    return game_dict