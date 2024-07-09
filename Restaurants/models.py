from django.db import models


class Restaurants(models.Model):
    resImage = models.URLField(max_length=1000, null=True)
    resName = models.CharField(max_length=200)
    estimated_time = models.CharField(max_length=20, default="30-40 min")
    menue = models.CharField(max_length=500)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    locality = models.CharField(max_length=500, default="VijayNagar Indore")
    offer = models.CharField(max_length=500, default="50% aboove ₹199")

    def __str__(self):
        return self.resName
    

