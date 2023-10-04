from .models import UserBankAccount,UserAddress
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from .constants import GENDER_TYPE,ACCCOUNT_TYPE
from django import forms 

# model er kaj complete korar pore form er kaj korte hobe..etokhone amra kaj ta backend theke korchi 
# ekhon to user k ekta form dite hobe jate kore user form ta submit korte pare 
class UserRegistrationForm(UserCreationForm): # amra modelForm use kortechi na ekhane karon amra user 
    # model use kortechi + amader likha model(userAddress,UserBankAccount) use kortechi jar karone ...
    # tie jehetu amra 3 ta alada alada form use korte parbo na jehetu 3 ta model use korchi  ...tie 
    # amra UserCreation form use kori 
    birth_date=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    # amra jate date dewar somoy ekta calender dekhte pay tar jonno ei widget ta likhte hoi 
    gender=forms.ChoiceField(choices=GENDER_TYPE)
    account_type=forms.ChoiceField(choices=ACCCOUNT_TYPE)
    street_address=forms.CharField(max_length=100)
    city=forms.CharField(max_length=100)
    postal_code=forms.IntegerField()
    country=forms.CharField(max_length=100)
    # 2 ta model er data amra niye aslam 
    # user amader j data gulo dibe segulo ekhane add kora holo bakigulo user dite parbe na 
    class Meta: # meta class ..class er moddhe extra characteristics add kore
        model=User # user model j use korchi er jonno form create korte hoi na er jonno sudhu call korlei hobe 
        fields=['username','password1','password2','first_name','last_name','email',
                'account_type','birth_date','gender','street_address','postal_code','city','country']
        # amra kon kon field gulo dekhte chay segulo ekhane likhte hobe .... ekhane (username,password,firstname)
        # ei field gulo amra kothao use kori nie egulo django amader provide korbe user model er maddhome
    def save(self,commit=True):
        our_user=super().save(commit=False) # ami database e data save korbo na ekhon
        if commit==True:
            our_user.save()  # user model er data save korlam
            account_type=self.cleaned_data.get('account_type')
            gender=self.cleaned_data.get('gender')
            postal_code=self.cleaned_data.get('postal_code')
            country=self.cleaned_data.get('country')
            birth_date=self.cleaned_data.get('birth_date')
            city=self.cleaned_data.get('city')
            street_address=self.cleaned_data.get('street_address')
            # user j amader form ta fillup korbe sekhan theke amra cleaned_data pabo . cleaned_data 
            # er moddhe amader data gulo thakbe ...sekhan theke amra sobgulo data(accounttype,gender...) 
            # pabo and data gulo ekhon amader save korte hobe  
            
            UserAddress.objects.create( # user ekta object create korlo 
                user=our_user,
                postal_code=postal_code,
                country=country,
                city=city,
                street_address=street_address
            )
            UserBankAccount.objects.create(
                user=our_user,
                account_type=account_type,
                gender=gender,
                birth_date=birth_date,
                account_no=100000+ our_user.id, 
            )
            # accountNo,balance,initial_deposit_date egula amra backend theke pabo 
        return our_user 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # super() use kortechi jehetu amra parent(usercreationForm) inherit kortechi ... super()diye
        # amra UserCreationForm k override kortechi 
        for field in self.fields:
            #print(field)
            self.fields[field].widget.attrs.update({ # field er jotogula class ache sobgula update hobe
                'class':( 
                    'appearance-none block w-full bg-gray-200'
                    'text-gray-700 border border-gray-200 rounded'
                    'py-3 px-4 leading-tight focus:outline-none'
                    'focus:bg-white focus:border-gray-500'
                )
            })
            
            
# profile e ki ki jinish update korte patebe amader user ei jonno ei form ta 
class UserUpdateForm(forms.ModelForm): # amra ekhon user er data gulo update korte cacchi jar karone 
    # model form use kortechi ..
    birth_date=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender=forms.ChoiceField(choices=GENDER_TYPE)
    account_type=forms.ChoiceField(choices=ACCCOUNT_TYPE)
    street_address=forms.CharField(max_length=100)
    city=forms.CharField(max_length=100)
    postal_code=forms.IntegerField()
    country=forms.CharField(max_length=100)
    # Normally amader j information gulo lagbe setar ekta form create korlam 
    
    class Meta:
        model=User
        fields=['first_name','last_name','email'] # amra user er sudhu ei field gulo change korte
        # dibo...tobe username and password soho bakifield gula apatoto change korte dibo na 
        
    def __init__(self, *args, **kwargs): # init mane hocche constructor 
        super().__init__(*args, **kwargs) # djangor j build in function ta ache tar moddhe j init function
        # ta chilo setake inherit kore niye aslam .ekhon amra setake override korbo nicher dewa 
        # backend er code ta diye
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class':(
                    'appearance-none block w-full bg-gray-200'
                    'text-gray-700 border border-gray-200 rounded'
                    'py-3 px-4 leading-tight focus:outline-none'
                    'focus:bg-white focus:border-gray-500'
                )
            })
            # jodi user er account/instance thake 
        if self.instance: # ekta object er instance thake
            try:
                user_account=self.instance.account
                user_address=self.instance.address
            except UserBankAccount.DoesNotExist:
                user_account = None # User er bank account nie mane tar account and address kono tai nie
                user_address = None
                
            if user_account: # jodi user er account thake taile sei user er age jemon user er registration
                #box ta khali thakto ekhon seta box fill up thakbe and initial ei data gulo fillup
                # thakbe 
                self.fields['account_type'].initial=user_account.account_type
                self.fields['gender'].initial=user_account.gender
                self.fields['birth_date'].initial=user_account.birth_date
                self.fields['street_address'].initial=user_address.street_address
                self.fields['city'].initial=user_address.city
                self.fields['postal_code'].initial=user_address.postal_code
                self.fields['country'].initial=user_address.country
                
                
    def save(self,commit=True): # jodi amader user tar first/last name update kore thake taile seta 
        # ei function diye save korbe 
        user=super().save(commit=False)
        if commit:
            user.save()
            
            user_account, created=UserBankAccount.objects.get_or_create(user=user)
            user_address, created=UserAddress.objects.get_or_create(user=user)
            # jodi oi user er account thake taile jabe user account e, ar jodi account na thake 
            #taile create hobe or seta created er moddhe jabe
            
            user_account.account_type=self.cleaned_data['account_type'] # user amader j form ta 
            # fillup korche tar datagulo ekhane niye asbo 
            user_account.gender=self.cleaned_data['gender']
            user_account.birth_date=self.cleaned_data['birth_date']
            user_account.save() # age amra data create korchilam ekhon amra create na kore save korbo
            
            user_address.street_address=self.cleaned_data['street_address']
            user_address.city=self.cleaned_data['city']
            user_address.postal_code=self.cleaned_data['postal_code']
            user_address.country=self.cleaned_data['country']
            user_address.save()
            
        return user 