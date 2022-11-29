from django.contrib import admin

from gamble.models import *
from .models import *


class gameAdmin(admin.ModelAdmin):
  list_display = ['sport','home','away','state']
  actions = ['turn_close','create_odds']

  def save_model(self,request,obj,form,change):
    super().save_model(request,obj,form,change)
    Odd.home(obj,0.0)
    Odd.away(obj,0.0)
    Odd.draw(obj,0.0) 


  @admin.action(description='Mark selected games as closed')
  def turn_close(self,request, queryset):
    games_id = [game.game_id for game in queryset]
    close = State.objects.get(state='closed')
    #update games to closed
    queryset.update(state=close)
    main_bets_list = set()

    #updating odds that happened
    for game_id in games_id:
      g = Game.objects.get(game_id=game_id)
      #mudar resultado da odd
      result = g.tabulate_winner()
      odd_type_result = Odd_type.objects.get(type=result)
      odd_type_home = Odd_type.objects.get(type='home')
      odd_type_draw = Odd_type.objects.get(type='draw')
      odd_type_away = Odd_type.objects.get(type='away')

      odd = Odd.objects.get(game=g,odd_type=odd_type_result)
      odd.turn_happened()
      odd.save()

      #tratar das bets
      bets_won = Bet_game.objects.filter(odd_id=odd)
      if odd_type_result == odd_type_home:
        odd_lost1 = Odd.objects.get(game=g,odd_type=odd_type_draw) 
        odd_lost2 = Odd.objects.get(game=g,odd_type=odd_type_away) 
      elif odd_type_result == odd_type_draw:
        odd_lost1 = Odd.objects.get(game=g,odd_type=odd_type_home) 
        odd_lost2 = Odd.objects.get(game=g,odd_type=odd_type_away) 
      else:
        odd_lost1 = Odd.objects.get(game=g,odd_type=odd_type_home) 
        odd_lost2 = Odd.objects.get(game=g,odd_type=odd_type_draw) 
      bets_lost1 = Bet_game.objects.filter(odd_id=odd_lost1)
      bets_lost2 = Bet_game.objects.filter(odd_id=odd_lost2)

      for bet in bets_won:
        main_bets_list.add(bet.bet.betID)
        bet.turn_won()
        bet.save()

      for bet in list(bets_lost1) + list(bets_lost2):
        main_bets_list.add(bet.bet.betID)
        bet.turn_lost()
        bet.save()

      for main_bet in main_bets_list:
        bet = Bet.objects.get(betID=main_bet)
        bet.check_status()
        bet.save() 
  
    

class oddAdmin(admin.ModelAdmin):
  list_display = ['game','odd_type','odd','happened']

admin.site.register(Sport)
admin.site.register(State)
admin.site.register(Odd_type)
admin.site.register(Game,gameAdmin)
admin.site.register(Odd,oddAdmin)
admin.site.register(Country)
admin.site.register(Competition)

# @admin.action(description='Mark selected stories as published')
# def make_published(modeladmin, request, queryset):
#     queryset.update(status='p')

# class ArticleAdmin(admin.ModelAdmin):
#     list_display = ['title', 'status']
#     ordering = ['title']
#     actions = [make_published]


# class ArticleAdmin(admin.ModelAdmin):
#     ...

#     actions = ['make_published']

#     @admin.action(description='Mark selected stories as published')
#     def make_published(self, request, queryset):
#         queryset.update(status='p')