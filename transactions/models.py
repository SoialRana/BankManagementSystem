from django.db import models
from accounts.models import UserBankAccount
from .constants import TRANSACTION_TYPE
# jehetu amra alada kore app use kortechi tie amader setting.py e giye alada kore bole dite hobe na 
# j amara static file use kortechi jodi amra ei static file ta app er moddhe declare kore thaki
# jemon amra core app e static file declare korchi jodi amra baire static file declare kortam taile
# amader app er moddhe bole dewa lagto ....

class Transactions(models.Model):
    account=models.ForeignKey(UserBankAccount,related_name='transactions',on_delete=models.CASCADE)
    #ekjon user er multiple transaction hote pare (se loan niteche,withdraw or deposit korteche)
    # tie one to many relation(Foreignkey)
    amount=models.DecimalField(max_digits=12,decimal_places=2)
    balance_after_transaction=models.DecimalField(max_digits=12,decimal_places=2)
    transaction_type=models.IntegerField(choices=TRANSACTION_TYPE,null=True)
    timestamp=models.DateTimeField(auto_now_add=True) # user jokhon loan nibe or jokhoin ekta 
    # transaction object toiri hobe tokhonoi time ta start hobe
    loan_approve=models.BooleanField(default=False)
    
    class Meta: #amader onek gulo transaction hote pare tie ei ordering transaction ta ke short korbe 
        ordering=['timestamp']