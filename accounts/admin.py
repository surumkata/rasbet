from django.contrib import admin
from accounts.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Session)
admin.site.register(Payment_method)
admin.site.register(Transation)
admin.site.register(History)
