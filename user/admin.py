from django.contrib import admin
from user.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'full_name', 'mobile_no']
    # readonly_fields = ('id',)

    # fieldsets = [
    #     # (None, {'fields': ['id','email', 'full_name', 'mobile_no','is_active','is_staff',]}),
    #     (None, {'fields': '__all__'}),
    # ]

admin.site.register(User, UserAdmin)
