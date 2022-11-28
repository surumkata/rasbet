import requests,json
from game.models import *



# Load ucras api data to databse
def load_ucras():
    print("Running job: load_ucras")
    url = "http://ucras.di.uminho.pt/v1/games/"
    games = requests.get(url).json()

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


