from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db import models
from config.settings import ALLOWED_IMAGE_EXTENSIONS

class CustomUser(AbstractUser):
    age = models.IntegerField(blank=True,null=True)
    profile_picture = models.ImageField(default='default.png')
    phone_num = models.IntegerField(unique=True,blank=True,null=True)
    friends = models.ManyToManyField('CustomUser', blank=True)


    def __str__(self):
        return self.username



