from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField(max_length=20, unique=True) #unique: 중복불가
    image = models.ImageField(upload_to='profile/', unique=True, null=True)
    message = models.CharField(max_length=100, null=True)
