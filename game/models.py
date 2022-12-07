from django.db import models
import requests
from datetime import datetime
import asyncio
from asgiref.sync import sync_to_async

class Sport(models.Model):
    sport = models.CharField(primary_key=True,max_length=50,null=False)
    has_draw = models.BooleanField()
    is_team_sport = models.BooleanField()

    def __str__(self):
        return self.sport


# on_hold | open | suspended | closed
class State(models.Model):
    state = models.CharField(primary_key=True,max_length=50,null=False)

    def __str__(self):
        return self.state

    def str(self):
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

class Participant(models.Model):
    name = models.CharField(primary_key=True,max_length=50,null=False)
    is_team = models.BooleanField()

    def __str__(self):
        return self.name


class Game(models.Model):
    game_id = models.AutoField(primary_key=True)
    # Specify what kind of sport
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    home = models.ForeignKey(Participant, on_delete=models.CASCADE,related_name='home')
    away = models.ForeignKey(Participant, on_delete=models.CASCADE,related_name='away')
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)
    datetime = models.DateTimeField()

    def home_scored(self,points):
        self.home_score += points

    def away_scored(self,points):
        self.away_score += points

    # Bets are possible
    def open(self):
        state = State.objects.get(state="open")
        self.state = state

    # Games finished by admin
    def close(self):
        state = State.objects.get(state="closed")
        self.state = state

    # Games is suspended, bets not possible
    def suspend(self):
        state = State.objects.get(state="suspended")
        self.state = state

    # Games unnaproved (specialist needs to aprove the game)
    def on_hold(self):
        state = State.objects.get(state="on_hold")
        self.state = state

    # Calculates the winner of the match at the moment
    def tabulate_winner(self):
        if self.home_score == self.away_score:
            return 'draw'
        elif self.home_score > self.away_score:
            return 'home'
        else:
            return 'away'

    @classmethod
    def exists(self,id):
        return Game.objects.filter(game_id=id).exists()

    def __str__(self):
        return f"{self.game_id}: {self.home} vs {self.away}"

    @classmethod
    def exist_game(self,home,away,datetime):
        return Game.objects.filter(home=home,away=away,datetime=datetime).exists()




    @classmethod
    # Create a game in the database
    def insert(self,sport,country,competition,home,away,datetime):
        # The sport MUST exist in the db

        if Sport.objects.filter(sport=sport).exists():
            sport = Sport.objects.get(sport=sport)
            country = Country.objects.get(country=country)
            competition = Competition.objects.get(competition=competition)
            home = Participant.objects.get(name=home)
            away = Participant.objects.get(name=away)
            # By default the game state is closed
            state = State.objects.get(state="on_hold")
            Game.objects.create(sport=sport,country=country,competition=competition,state=state,home=home,away=away,datetime=datetime)




class Odd(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    odd_type = models.ForeignKey(Odd_type, on_delete=models.CASCADE)
    odd = models.FloatField()
    happened = models.BooleanField(default=False)
    number_betters = models.IntegerField(default=0)

    @classmethod
    # Create odd to the outcome home team wins
    def home(self,game,odd):
        type = Odd_type.objects.get(type="home")
        if not (Odd.objects.filter(game=game,odd_type=type).exists()):
            Odd.objects.create(game=game,odd_type=type,odd=odd)
        else:
            odd_to_update = Odd.objects.get(game=game,odd_type=type)
            odd_to_update.odd = odd
            odd_to_update.save()

    @classmethod
    # Create odd to the outcome away team wins
    def away(self,game,odd):
        type = Odd_type.objects.get(type="away")
        if not (Odd.objects.filter(game=game,odd_type=type).exists()):
            Odd.objects.create(game=game,odd_type=type,odd=odd)
        else:
            odd_to_update = Odd.objects.get(game=game,odd_type=type)
            odd_to_update.odd = odd
            odd_to_update.save()

    @classmethod
    # Create odd to the outcome draw
    def draw(self,game,odd):
        type = Odd_type.objects.get(type="draw")
        if not (Odd.objects.filter(game=game,odd_type=type).exists()):
            Odd.objects.create(game=game,odd_type=type,odd=odd)
        else:
            odd_to_update = Odd.objects.get(game=game,odd_type=type)
            odd_to_update.odd = odd
            odd_to_update.save()

    def create(self,game_id,odd_type,odd):
        game = Game.objects.get(id=game_id)
        Odd.objects.create(game=game,odd_type=odd_type,odd=odd)

    def incr_number_better(self):
        self.number_betters+=1


    #change odd value
    def change_odd(self,value:float):
        self.odd = value

    #change odd to happened
    def turn_happened(self):
        self.happened = True

    def __str__(self):
        return str(self.game) + '    '+ str(self.odd_type)




def detail_games(games,ordered_by_nb):
    games_dict = {}
    datetimes = set()
    for g in games:
        details = open_game_details(g)
        if details!={}:
            datetime = g.datetime.date().strftime("%Y/%m/%d")
            datetimes.add(datetime)
            if datetime in games_dict:
                games_dict[datetime].append(details)
            else: 
                games_dict[datetime] = [details]

    for datetime in datetimes:
        if(ordered_by_nb): games_dict[datetime].sort(key=take_number_betters,reverse=True)
        else: games_dict[datetime].sort(key=take_datetime)

    return games_dict


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

def open_game_details(game):
    odds = Odd.objects.filter(game_id=game.game_id)
    game = Game.objects.get(game_id=game.game_id)

    if game.state.str() == "open":
        game_dict = {}
        game_dict["game"] = game
        total_betters = 0
        for odd_obj in odds:
            type =  getattr(odd_obj, "odd_type")
            odd = getattr(odd_obj, "odd")
            number_betters = getattr(odd_obj,"number_betters")
            total_betters += number_betters
            if str(type) == "home":
                game_dict["home_odd"] = odd
                game_dict["home_nb"] = number_betters
            elif str(type) == "away":
                game_dict["away_odd"] = odd
                game_dict["away_nb"] = number_betters
            elif str(type) == "draw":
                game_dict["draw_odd"] = odd
                game_dict["draw_nb"] = number_betters
        if total_betters > 0:
            game_dict["home_nb"] = float("{:.2f}".format(game_dict["home_nb"] / total_betters * 100))
            game_dict["draw_nb"] = float("{:.2f}".format(game_dict["draw_nb"] / total_betters * 100))
            game_dict["away_nb"] = float("{:.2f}".format(game_dict["away_nb"] / total_betters * 100))
        game_dict["nb"] = total_betters
        return game_dict
    else:
        return {}

def take_number_betters(elem):
    return elem["nb"]

def take_datetime(elem):
    return elem["game"].datetime

#list of the sports, countries that have it and respective competitions
def sports_list():
    sports = Sport.objects.all()
    sports_listing = {}
    countrys = Country.objects.all()
    for sport in sports:
        sport_name = sport.sport
        sports_listing[sport_name] = {}
        for country in countrys:
            country_name = country.country
            sports_listing[sport_name][country_name] = [str(k) for k in Competition.objects.filter(sport=sport,country=country)] 
    return sports_listing





def db_change_gamestate(game_id,state):
    try:
        if(Game.exists(game_id)):
            g = Game.objects.get(game_id=game_id)
            if(state == 'open'):
                g.open()
                g.save()
            elif(state == 'closed'):
                g.close()
                g.save()
            elif(state == 'suspended'):
                g.suspend()
                g.save()
            elif(state == 'on_hold'):
                g.on_hold()
                g.save()
    except Exception as e:
        print(e)

def db_change_gameodd(game_id,value,odd_type):
    try:
        odd_type = Odd_type.objects.get(type=odd_type)
        if Odd.objects.filter(game=game_id,odd_type=odd_type).exists():
            odd = Odd.objects.get(game=game_id,odd_type=odd_type)
            odd.change_odd(float(value))
            odd.save()
        else:
            Odd.create(game_id,odd_type,float(value))


    except Exception as e:
        print(e)
