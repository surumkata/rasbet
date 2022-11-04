from django.db import models
import requests
from datetime import datetime



class Sport(models.Model):
    sport = models.CharField(primary_key=True,max_length=50,null=False)
    has_draw = models.BooleanField()
    is_team_sport = models.BooleanField()

    def __str__(self):
        return self.sport


# open | suspended | closed
class State(models.Model):
    state = models.CharField(primary_key=True,max_length=50,null=False)

    def __str__(self):
        return self.state

# home | away | draw ...
class Odd_type(models.Model):
    type = models.CharField(primary_key=True,max_length=50,null=False)

    def __str__(self):
        return self.type

class Country(models.Model):
    country = models.CharField(primary_key=True,max_length=50,null=False)

    def __str__(self):
        return self.country


class Competition(models.Model):
    competition = models.CharField(primary_key=True,max_length=50,null=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)

    def __str__(self):
        return self.competition


class Game(models.Model):
    game_id = models.CharField(max_length=50,primary_key=True)
    # Specify what kind of sport
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
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
    @classmethod
    def open(self):
        state = State.objects.get(state="open")
        self.state = state

    # Games has not started yet,bets not possible
    @classmethod
    def close(self):
        state = State.objects.get(state="closed")
        self.state = state

    # Games is suspended, bets not possible
    @classmethod
    def suspend(self):
        state = State.objects.get(state="suspended")
        self.state = state

    # Game finished , bets not possible
    def finish(self):
        state = State.objects.get(state="finish")
        self.state = state

    @classmethod
    def exists(self,id):
        return Game.objects.filter(game_id=id).exists()




    @classmethod
    # Create a game in the database
    def create(self,id,sport,country,competition,home,away,datetime):
        # The sport MUST exist in the db
        if Sport.objects.filter(sport=sport).exists():
            sport = Sport.objects.get(sport=sport)
            country = Country.objects.get(country=country)
            competition = Competition.objects.get(competition=competition)
            # By default the game state is closed
            state = State.objects.get(state="closed")
            Game.objects.create(game_id=id,sport=sport,country=country,competition=competition,state=state,home=home,away=away,datetime=datetime)




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
                Game.create(g['id'],"football","Portugal","Primeira Liga",g['homeTeam'],g['awayTeam'],game_date_obj)
                game = Game.objects.get(game_id=g['id'])
                Odd.home(game,g['bookmakers'][1]['markets'][0]['outcomes'][0]['price'])
                Odd.away(game,g['bookmakers'][1]['markets'][0]['outcomes'][1]['price'])
                Odd.draw(game,g['bookmakers'][1]['markets'][0]['outcomes'][2]['price'])


def game_details(game:dict):
    odds = Odd.objects.filter(game_id=game['game_id'])
    game = Game.objects.get(game_id=game['game_id'])
    sport = str(game.sport)
    country = str(game.country)
    competition = str(game.competition)
    state = str(game.state)
    game_dict = {}
    game_dict["game"] = game
    for odd_obj in odds:
        type =  getattr(odd_obj, "odd_type")
        odd = getattr(odd_obj, "odd")
        if str(type) == "home":
            game_dict["home_odd"] = odd
        elif str(type) == "away":
            game_dict["away_odd"] = odd
        elif str(type) == "draw":
            game_dict["draw_odd"] = odd
    game_dict["sport"] = sport
    game_dict["country"] = country
    game_dict["competition"] = competition
    game_dict["state"] = state
    return game_dict




def sports_list():
    sports = Sport.objects.all().values()
    sports_listing = []
    for sport in sports:
      sports_listing.append(sport['sport'])
    return sports_listing



def db_change_games_state(games_to_change):
    print(games_to_change)
    for game in games_to_change:
        if Game.exists(game[0]):
            g = Game.objects.get(game_id=game[0])
            print(g)
            if game[1] == 'Closed':
                g.state = State.objects.get(state="closed")
                g.save()
            elif game[1] == 'Open':
                g.state = State.objects.get(state="open")
                g.save()
            elif game[1] == 'Suspended':
                g.state = State.objects.get(state="suspended")
                g.save()

