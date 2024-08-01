
from django.db import models
class Restaurant(models.Model):
    resImage = models.URLField(max_length=1000, null=True)
    resName = models.CharField(max_length=200, default='none')
    estimated_time = models.CharField(max_length=20, default="30-40 min")
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    locality = models.CharField(max_length=500, default="VijayNagar Indore")
    offer = models.CharField(max_length=500, default="50% above ₹199")

    def __str__(self):
        return self.resName

class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='menu_items', on_delete=models.CASCADE)
    productName = models.CharField(max_length=100, default='Unnamed Product')
    price = models.CharField(max_length=4)
    description = models.CharField(max_length=200)
    productImage = models.URLField(null=True)

    def __str__(self):
        return self.productName
