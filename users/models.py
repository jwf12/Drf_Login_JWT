from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=30, unique=True)
    
    def __str__(self):
        return self.username
    