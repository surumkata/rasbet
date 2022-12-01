from django.contrib import admin
from accounts.models import *



class TransationAdmin(admin.ModelAdmin):
  list_display = ['user','type']

class UserAdmin(admin.ModelAdmin):
  list_display = ['first_name','last_name','email','birthday','balance']


class SpecAdmin(admin.ModelAdmin):
  list_display = ['specID','userID']

class HistoryAdmin(admin.ModelAdmin):
  list_display = ['bet','user']

class PromotionAdmin(admin.ModelAdmin):
  list_display = ['promo_code','value_restriction','mail_template_path','image_path','limit_date']

  def save_model(self,request,obj,form,change):
    super().save_model(request,obj,form,change)
    email_list = []
    users = User.objects.all()
    for user in users:
      email_list.append(user.email)
    mail = SendingEmail(obj.mail_template_path)
    mail.send(email_list)

class BetPromotionAdmin(admin.ModelAdmin):
  list_display = ['promo_code','applyable_game','reward']

class DepositPromotionAdmin(admin.ModelAdmin):
  list_display = ['promo_code','reward','usages','first_deposit_restriction']

# Register your models here.
admin.site.register(User,UserAdmin)
admin.site.register(Specialist,SpecAdmin)
admin.site.register(Session)
admin.site.register(Payment_method)
admin.site.register(Transation,TransationAdmin)
admin.site.register(History,HistoryAdmin)
admin.site.register(Promotion,PromotionAdmin)
admin.site.register(Bet_Promotion,BetPromotionAdmin)
admin.site.register(Deposit_Promotion,DepositPromotionAdmin)
admin.site.register(FavoriteSports)
admin.site.register(FavoriteCompetitions)
admin.site.register(FavoriteParticipants)
