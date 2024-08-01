from django.db import models
from django.conf import settings

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_payment_intent_id = models.CharField(max_length=255)
    amount = models.IntegerField()
    currency = models.CharField(max_length=10)
    STATUS_CHOICES = [
        ('requires_payment_method', 'Requires Payment Method'),
        ('requires_confirmation', 'Requires Confirmation'),
        ('requires_action', 'Requires Action'),
        ('processing', 'Processing'),
        ('requires_capture', 'Requires Capture'),
        ('canceled', 'Canceled'),
        ('succeeded', 'Succeeded'),
    ]
    
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
       
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.user} - {self.status}"





  
