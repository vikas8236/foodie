from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        # read_only_fields = ['id', 'user', 'stripe_payment_intent_id', 'status', 'created_at']
