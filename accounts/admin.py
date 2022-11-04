from django.contrib import admin
from accounts.models import *



class TransationAdmin(admin.ModelAdmin):
  list_display = ['user','type']

class AdminAdmin(admin.ModelAdmin):
  list_display = ['adminID','userID']

class SpecAdmin(admin.ModelAdmin):
  list_display = ['specID','userID']

# Register your models here.
admin.site.register(User)
admin.site.register(Admin,AdminAdmin)
admin.site.register(Specialist,SpecAdmin)
admin.site.register(Session)
admin.site.register(Payment_method)
admin.site.register(Transation,TransationAdmin)
admin.site.register(History)

