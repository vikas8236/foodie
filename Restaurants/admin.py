from django.contrib import admin
from .models import Restaurant, MenuItem


class RestaurantAdmin(admin.ModelAdmin):
    search_fields = ['resName', 'locality', 'rating', 'offer']

    
class MenuItemAdmin(admin.ModelAdmin):
    search_fields = ['productName']    

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(MenuItem)




