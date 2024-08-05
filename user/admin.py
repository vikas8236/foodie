from django.contrib import admin
from user.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'mobile_no']
    search_fields = ['email', 'first_name']
   
admin.site.register(User, UserAdmin)
