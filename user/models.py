import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from user.managers import UserManager
from products.models import Product

class BaseModel(models.Model):
    id = models.UUIDField(primary_key = True, editable = False, default = uuid.uuid4)

    class Meta:
        abstract = True

class User(AbstractUser, BaseModel):
    username = None
    # full_name = models.CharField(max_length = 200)
    # first_name = models.CharField(max_length=100)
    # last_name = models.CharField(max_length=100)
    email = models.EmailField(unique = True, max_length = 100)
    mobile_no = models.CharField(max_length = 15)
    profileImg = models.URLField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    # def save(self, *args, **kwargs):
    #     if not self.full_name:
    #         self.full_name = f"{self.first_name} {self.last_name}".strip()
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.email
    



class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    products = models.ManyToManyField(Product, related_name='carts', blank=True)

    def __str__(self):
        return f"Cart for {self.user.username}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)   


    def __str__(self): 
        return self.quantity    

    

