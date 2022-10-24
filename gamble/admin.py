from django.contrib import admin
from gamble.models import Bet_type,Bet,History


admin.site.register(Bet_type)
admin.site.register(Bet)
admin.site.register(History)
