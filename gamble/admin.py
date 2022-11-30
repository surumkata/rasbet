from django.contrib import admin
from gamble.models import *


class betAdmin(admin.ModelAdmin):
  list_display = ['betID','type','amount','datetime']


class bet_gameAdmin(admin.ModelAdmin):
  list_display = ['bet','odd_id','odd','status']

admin.site.register(Bet,betAdmin)
admin.site.register(Bet_type)
admin.site.register(Bet_game,bet_gameAdmin)
admin.site.register(Bet_status)
