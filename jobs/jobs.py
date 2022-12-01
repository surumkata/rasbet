import requests,json
from game.models import *
from django.utils.timezone import make_aware



# Load ucras api data to databse
def load_ucras():
    print("Running job: load_ucras")
    url = "http://ucras.di.uminho.pt/v1/games/"
    games = requests.get(url).json()

    if not Sport.objects.filter(sport="Football").exists():
        Sport.objects.create(sport="Football",has_draw=True,is_team_sport=True)

    if not Country.objects.filter(country="Portugal").exists():
        Country.objects.create(country="Portugal")

    if not Competition.objects.filter(competition="Primeira Liga").exists():
        sport = Sport.objects.get(sport="Football")
        country = Country.objects.get(country = "Portugal")
        Competition.objects.create(competition="Primeira Liga",country=country,sport=sport)

    for g in games:
        # Only new games are added

        if not Participant.objects.filter(name=g['homeTeam']).exists():
            Participant.objects.create(name=g['homeTeam'],is_team=True)
        if not Participant.objects.filter(name=g['awayTeam']).exists():
            Participant.objects.create(name=g['awayTeam'],is_team=True)

        try:

            home = Participant.objects.get(name=g['homeTeam'])
            away = Participant.objects.get(name=g['awayTeam'])

            game_date_obj = datetime.strptime(g['commenceTime'][:-8],"%Y-%m-%dT%H:%M")
            if not Game.exist_game(home,away,game_date_obj):

                now = datetime.now().replace(second= 0, microsecond= 0)

                # Only upcoming games are added
                if game_date_obj>now:
                    Game.insert("Football","Portugal","Primeira Liga",g['homeTeam'],g['awayTeam'],game_date_obj)
                    game = Game.objects.filter(home=home,away=away,datetime=game_date_obj).get()
                    Odd.home(game,g['bookmakers'][1]['markets'][0]['outcomes'][0]['price'])
                    Odd.away(game,g['bookmakers'][1]['markets'][0]['outcomes'][1]['price'])
                    Odd.draw(game,g['bookmakers'][1]['markets'][0]['outcomes'][2]['price'])
        except Exception as e:
            print(e)

def close_started_games():
    print("Running job: suspending started games")
    games = Game.objects.filter(datetime__lte=datetime.now())
    for game in games:
        game.suspend()
        game.save()
