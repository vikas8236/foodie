from django.contrib import admin
from products.models import Product

class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name', 'description']

admin.site.register(Product, ProductAdmin)

