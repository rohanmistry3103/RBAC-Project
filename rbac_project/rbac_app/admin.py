from django.contrib import admin

# Register your models here.
from .models import CustomUser,UserAPIAccess,API

admin.site.register(CustomUser)
admin.site.register(API)
admin.site.register(UserAPIAccess)

