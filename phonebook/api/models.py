from django.db import models
from django.contrib.auth.models import User

class Contact(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    spam = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    phone_number = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return str(self.user)