from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  
from django.conf import settings
from django.utils.text import slugify
from django.utils.crypto import get_random_string
# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=225)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=10)
    password = models.CharField(max_length=200,null=True)

   

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()


class Stock(models.Model):
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class Sales(models.Model):
    product = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity_sold = models.PositiveIntegerField()
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    product = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity_ordered = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)



class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
