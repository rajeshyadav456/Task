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
    USER_TYPE_CHOICES = [
        ('DEVELOPER', 'Developer'),
        ('MANAGER', 'Manager'),
    ]
    username = models.CharField(unique=True, max_length=225)
    password = models.CharField(max_length=200,null=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

   

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = UserManager()

class Task(models.Model):
    STATUS_CHOICES = [
        ('TODO', 'Todo'),
        ('IN_PROGRESS', 'In Progress'),
        ('DONE', 'Done'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    assignee = models.ForeignKey('User', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TODO')

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
