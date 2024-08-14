from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserBankAccount(models.Model):
    user=models.OneToOneField(User,related_name='account',on_delete=models.CASCADE)
    accountNo=models.IntegerField(unique=True,null=True)
    balance=models.DecimalField(default=0,max_digits=10,decimal_places=2)

    def __str__(self):
        return f'acNo: {self.accountNo}'
