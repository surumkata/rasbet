from django.contrib import admin
from accounts.models import *



class TransationAdmin(admin.ModelAdmin):
  list_display = ['user','type']

class UserAdmin(admin.ModelAdmin):
  list_display = ['first_name','last_name','email','birthday','balance']

class AdminAdmin(admin.ModelAdmin):
  list_display = ['adminID','userID']

class SpecAdmin(admin.ModelAdmin):
  list_display = ['specID','userID']

class HistoryAdmin(admin.ModelAdmin):
  list_display = ['bet','user']

class PromotionAdmin(admin.ModelAdmin):
  list_display = ['promo_code','value_restriction','mail_template_path','image_path','limit_date']

class BetPromotionAdmin(admin.ModelAdmin):
  list_display = ['promo_code','applyable_game','reward']

class DepositPromotionAdmin(admin.ModelAdmin):
  list_display = ['promo_code','reward','usages','first_deposit_restriction']

# Register your models here.
admin.site.register(User,UserAdmin)
admin.site.register(Admin,AdminAdmin)
admin.site.register(Specialist,SpecAdmin)
admin.site.register(Session)
admin.site.register(Payment_method)
admin.site.register(Transation,TransationAdmin)
admin.site.register(History,HistoryAdmin)
admin.site.register(Promotion,PromotionAdmin)
admin.site.register(Bet_Promotion,BetPromotionAdmin)
admin.site.register(Deposit_Promotion,DepositPromotionAdmin)

