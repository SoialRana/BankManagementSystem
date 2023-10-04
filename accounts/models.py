from django.db import models
from django.contrib.auth.models import User
from .constants import GENDER_TYPE,ACCCOUNT_TYPE
# Create your models here.


# django amaderke build in user make korar facility
#(USER, backentd)
class UserBankAccount(models.Model):# models .model k inherit korlam jate kore ei model er sob kisu use korte pari amra
    
    user=models.OneToOneField(User,related_name='account',on_delete=models.CASCADE) # amader j build in user ache tar sathe relation  build kortechi
    # django j amader k User(username,first_name,last_name,password...) model ta diche tar sathe ami j model
    # build korbo seta one to one field hobe 
    # related name use kortechi jate ami ei name use kore user model er data(username,first/last_name) access korte pari 
    # on_delete= ei user er joto data ache (street,city,birth,country) sob delete hoye jabe 
    account_type=models.CharField(max_length=10,choices=ACCCOUNT_TYPE)
    account_no=models.IntegerField(unique=True) # account no 2 jon userer same hote parbe na 
    birth_date=models.DateField(null=True,blank=True) #kew jodi birth date na dite chay amra take jor korbo na tie null=True
    gender=models.CharField(max_length=10,choices=GENDER_TYPE)
    initial_deposite_date=models.DateField(auto_now_add=True) # ei user first time kokhon account khulche seta amra track rakhte chay 
    # jokhoinoi account khulbe tokhnoi time ta show korbe 
    balance=models.DecimalField(default=0,max_digits=12,decimal_places=2)
    # ek jon user 12 digit obdi taka rakhte parbe . dui doshomik ghor obdi rakhte parebe
    def __str__(self):
        return f'Account no: {self.account_no}'
    
    
class UserAddress(models.Model):
    user=models.OneToOneField(User,related_name='address',on_delete=models.CASCADE)
    # amader address model er sathe user model er somporko hocche one to one field 
    street_address=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    postal_code=models.IntegerField()
    country=models.CharField(max_length=100)
    
    # super user create na korle admin panel kaj korbe na ...
    
    def __str__(self):
        return str(self.user.email) # uporer function ei function same kaj korbe
    
    