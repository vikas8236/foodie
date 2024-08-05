from django.contrib import admin
from .models import Payment

class PaymentAdmin(admin.ModelAdmin):
    search_fields = ['user__email','stripe_payment_intent_id', 'amount', 'status', 'created_at', 'currency']



admin.site.register(Payment, PaymentAdmin)