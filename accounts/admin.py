from django.contrib import admin
from accounts.models import User,Transation,Payment_method

# Register your models here.
admin.site.register(User)
admin.site.register(Payment_method)
admin.site.register(Transation)
