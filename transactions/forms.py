from django import forms
from .models import Transactions

class TransactionForm(forms.ModelForm):
    class Meta:
        model=Transactions
        fields=['amount','transaction_type'] # amader user sudhu amount ta dibe, transaction type
        # ta amra backend theke diye dibo or dekhbo ....amra transaction model er sobgula data user k dekhabo na 
    def __init__(self, *args, **kwargs): # jehetu amra amount ta backend theke diye dibo tie amader
        # kisu extra code likhte hobe ..jehetu transaction type ta visible thakbe or select korar
        # option thakbe tie amra init function k call kortechi  
        #amra kwargs er moddhe build in kisu pass korbo . amra etake normal rakhtechi 
        # karon jokhon amra deposit,withdraw form er kaj korbo tokhon use korbo . onek gulo parameter
        # theke amra accounttake ber kore nibo 
        self.account=kwargs.pop('account')  # account value k pop kore anlam. ei account ta hocche user er bank account
        super().__init__(*args, **kwargs) # amra override korbo ei jonno super use kori
        self.fields['transaction_type'].disabled=True # ei field disable thakbe 
        self.fields['transaction_type'].widget=forms.HiddenInput() #user er theke hide kora 
        # thakbe mane user dekhte parbe na 
        
    def save(self,commit=True): 
        self.instance.account=self.account # jei user ta request korteche tar jodi kono obj database thake sei instance er 
        # account e jabo , account giye amra self.account rakhte pari  
        self.instance.balance_after_transaction=self.account.balance # jei user request korteche 
        # tar account giye balance ta rakhbo...jeta balance after transaction er moddhe show korbe 
        return super().save()
    
    
class DepositForm(TransactionForm): # transaction form k inherit korbe
    def clean_amount(self): # jodi amra kono field k filter or search korte chay taile clean_ diye 
        # jei field er upor korte cacchi tar nam dibo...ekhane amount field ke filter korbo
        # jodi balance k niye kaj korte chay taile clean_balance likhbo  ..amount field korbo
        min_deposit_amount=100 # min 100 taka deposit kortei hobe 
        amount=self.cleaned_data.get('amount') #user er fillup kora form theke amra amount
        # field er value k niye ashlam
        if amount<min_deposit_amount:
            raise forms.ValidationError(
                f'You need to deposit at least {min_deposit_amount} $'
            )
        # kokhon kon type er error use korbo amra seta google e search diye pora 
        return amount # raise hocche error k show korar jonno ekta build in keyword
    
    
class WithdrawForm(TransactionForm):
    def clean_amount(self):
        account=self.account # user er bank account ta amra acount er moddhe rakhlam 
        min_withdraw_amount=500
        max_withdraw_amount=20000
        balance=account.balance #1000
        amount=self.cleaned_data.get('amount') # amra amader amount er j field ta chilo user fillup korbe amra seita capture korbo 
        if amount<min_withdraw_amount:
            raise forms.ValidationError(f'You can withdraw at least {min_withdraw_amount} $')
        if amount>max_withdraw_amount:
            raise forms.ValidationError(f'You can withdraw at most {max_withdraw_amount} $')
        
        if amount>balance:
            raise forms.ValidationError(f'You have {balance}$ in your account. '
                                        'You can not withdraw more than your account balance ')
            
        return amount
    
    
class LoanRequestForm(TransactionForm):
    def clean_amount(self): 
        amount=self.cleaned_data.get('amount')
        return amount