from django.db import models
from django.contrib.auth.models import AbstractUser
from users.models import CustomUser





class Friend_Request(models.Model):
    from_user = models.ForeignKey(
        CustomUser, on_delete= models.CASCADE,related_name='from_user')
    to_user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='to_user')

    def __str__(self):
        return f'{self.from_user} to {self.to_user}'
