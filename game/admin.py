from django.contrib import admin
from .models import *


class gameAdmin(admin.ModelAdmin):
  list_display = ['sport','home','away','sate']

admin.site.register(Sport)
admin.site.register(State)
admin.site.register(Odd_type)
admin.site.register(Game,gameAdmin)
admin.site.register(Odd)
admin.site.register(Country)
admin.site.register(Competition)
