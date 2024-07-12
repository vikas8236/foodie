from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product
from products.serializers import ProductSerializer

import stripe

stripe.api_key = 'sk_test_51PbgshRohX98q0M7Kjnp5WHQdFqYTyvRHoYpbaHPDisqHkxTUIFq8g9J2B7c8x2Z7ROdJzmFi4Qjlw8JSJueKwDX00Y8MiJtnb'

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'updated_at', 'total_price', 'items', 'paid']


class CheckoutSerializer(serializers.Serializer):
    items = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField()
        )
    )

    def create(self, validated_data):
        user = self.context['request'].user
        items_data = validated_data.pop('items')
        
        order = Order.objects.create(user=user, total_price=0)

        total_price = 0
        for item_data in items_data:
            product_id = item_data.get('product_id')
            quantity = item_data.get('quantity')
            product = Product.objects.get(id=product_id)
            total_price += product.price * quantity
            OrderItem.objects.create(order=order, product=product, quantity=quantity)
        
        order.total_price = total_price

        payment_intent = stripe.PaymentIntent.create(
            amount=int(total_price * 100),  # Stripe expects amount in cents
            currency='usd',
            metadata={'order_id': order.id}
        )

        order.stripe_payment_intent = payment_intent['id']
        order.save()

        return order
