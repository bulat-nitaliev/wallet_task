from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):...


class Wallet(models.Model):
    uuid = models.UUIDField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    balance = models.IntegerField(default=0)  

    def __str__(self):
        return f"Wallet {self.uuid} with balance {self.balance}"