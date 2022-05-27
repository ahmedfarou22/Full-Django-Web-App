from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Searches(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,)
    avsearches = models.IntegerField(null=True)

    def __str__(self):
        stringav = str(self.avsearches)
        return stringav





# class User(models.Model):
#     name = models.CharField(max_length=100)
#     username = models.CharField(max_length=50, unique=True)
#     password = models.CharField(max_length=32)
#     email = models.EmailField(max_length=50, unique=True)
#     date_registered = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return self.username