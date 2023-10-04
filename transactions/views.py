from typing import Any, Dict
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views import View
from datetime import datetime
from django.db.models import Sum
from django.http import HttpResponse
from django.views.generic import CreateView,ListView
from transactions.constants import DEPOSIT,WITHDRAWAL,LOAN,LOAN_PAID
from transactions.forms import(
    DepositForm,
    WithdrawForm,
    LoanRequestForm,
)
from transactions.models import Transactions

# Create your views here.

# amra transactionCreatemixin name ekta class create korchi jeta inherit kore amra aamrder baki transaction gulo korbo
class TransactionCreateMixin(LoginRequiredMixin,CreateView):
    # TransactionCreateMixin use korte gele must be amader user k login hoite hobe 
    # jehetu amra transaction ta toiri kortechi mane se loan nile / or deposit korle ekta
    # obj toiri kortechi tie create view use korbo
    template_name='transactions/transaction_form.html'
    model=Transactions
    title=''
    success_url=reverse_lazy('transaction_report')
    
    def get_form_kwargs(self): #ei function er moddhe amra besh kichu function k pass kore dibo 
        kwargs=super().get_form_kwargs() #jeta amra super.get_form_kwargs theke save korbo 
        kwargs.update({ # save korar por amra update kore dibo account 
            'account': self.request.user.account
        })
        return kwargs
    
    def get_context_data(self, **kwargs): # amra jokhon form use kortam tokhon context data pass
        # kortam kintu ekhon jehetu class use kortechi tie get_context function use korte hoi
        context=super().get_context_data(**kwargs) #tamplate e context data pass kora
        context.update({
            'title': self.title # context er moddhe amra title ta ke pass kore dichi
        })# kon template er form ta amra use kortechi seta pass kore dibo
        return context
    
    
class DepositMoneyView(TransactionCreateMixin): #deposit korte gele ekjon user k login hoite hobe 
    form_class=DepositForm
    title='Deposit'
    
    def get_initial(self): # deposit menu te click korle choto ekta form pacche amount diye dile
        # de deposit hoye jacche 
        initial={'transaction_type':DEPOSIT} # jehetu transaction type j deposit seta se dekhte 
        # dicche na tie get initial function diye amra bole dicchi j amader transaction type ta deposit 
        return initial
    
    def form_valid(self,form):
        amount=form.cleaned_data.get('amount') # first e amra user er amount ta nilam 
        print('helllo',amount)
        account=self.request.user.account # erpor user er kon account seta dilam 
        # if not account.initial_deposit_date: # jodi user er initial deposit date na thake 
        #     now=timezone.now()
        #     account.initial_deposit_date=now
        account.balance+=amount # amount = 200, tar ager balance = o taka, new balance = 0+200 = 200 taka
        account.save( # account ta jokhon save korbo tokhon sudhu balance ta ke update korbo python dictionary theke 
            update_fields=[
                # 'initial_deposit_date',
                'balance'
            ]
        )
        print('helllo',account.balance)
        messages.success( # user k amra ekta message show koralam j tar eto taka deposit hoiche 
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
        )
        return super().form_valid(form) # finally form valid return kore dichi 
    
    
class WithdrawMoneyView(TransactionCreateMixin):
    form_class=WithdrawForm
    title='Withdraw Money'
    
    def get_initial(self): # eta amra backend theke bole dicchi j amader transaction type ta withdrawl 
        # na hole user transaction korte thakbe korte thakbe tokhon amra track korte parbo na 
        initial={'transaction_type': WITHDRAWAL}
        return initial
    
    def form_valid(self,form):
        amount=form.cleaned_data.get('amount')
        self.request.user.account.balance -= form.cleaned_data.get('amount')
        # amader balance theke amra sudhu amader withdrawl amount ta komay dicchi 
        # balance =300
        # amount= 5000
        self.request.user.account.save(update_fields=['balance'])
        
        messages.success(
            self.request,
            f'successfully withdrawn {"{:,.2f}".format(float(amount))}$ from your account'
        )
        return super().form_valid(form)
    
    
    
class LoanRequestView(TransactionCreateMixin):
    form_class=LoanRequestForm
    title='Request For Loan'
    
    def get_initial(self):
        initial={'transaction_type': LOAN}
        return initial
    
    def form_valid(self,form):
        amount=form.cleaned_data.get('amount')
        current_loan_count=Transactions.objects.filter(
            account=self.request.user.account,transaction_type=3,loan_approve=True).count()
        # amra transaction ta k filter kortechi ei jonno j amader user max 3 bar loan nite parbe or max se 3 
        # bar loan request korte parbe ....jodi transaction_type=3 and loan_approved=True hoi taile seta .count diye oi modeler obj k
        # filter korle j value gulo pabo seta pai amra 
        if current_loan_count>=3:
            return HttpResponse("You have cross the loan limits")
        messages.success(
            self.request,
            f'Loan request for {"{:,.2f}".format(float(amount))}$ submitted successfully'
            # tomar loan request form ta submit hoiche but approve hoi nie 
        )
        return super().form_valid(form)
    
    
class TransactionReportView(LoginRequiredMixin,ListView):
    template_name='transactions/transaction_report.html'
    model=Transactions
    # form_data={}
    balance=0 #filter korar pore ba age amar total balance ke show korbe
    def get_queryset(self): # get queryset diye amra user er account theke jotogulo transaction hoiche segulo filter kortechi 
        queryset=super().get_queryset().filter(account=self.request.user.account)
        start_date_str=self.request.GET.get('start_date') # frontend theke start and end date ...kon date theke kon date  user report dekhte chay tar ekta report dilam 
         # eta amra frontend theke dekhbo karon backend theke amra kono form make korini 
        end_date_str=self.request.GET.get('end_date')
        
        if start_date_str and end_date_str: # jodi start and end 2 tai thake ..must thakte hobe 
            start_date=datetime.strptime(start_date_str,'%Y-%m-%d').date()
            end_date=datetime.strptime(end_date_str,'%Y-%m-%d').date()
            # date gulo k amra strptime e konvert korlam 
            
            queryset=queryset.filter(timestamp__date__gte=start_date,timestamp__date__lte=end_date)
            # timestamp er moddhe ekta function ache date__gte and date__lte jodi egulo amader start date theke beshi hoi 
            # and end date theke kom hoi taile amra queryset er moddhe data pabo 
            self.balance=Transactions.objects.filter(
                timestamp__date__gte=start_date,timestamp__date__lte=end_date
            ).aggregate(Sum('amount'))['amount__sum'] # multiple function jokhon amader user korar dorkar hoi tokhon aggregate use kori 
            # modeler value gulo jokhon sum korar dorkar pore tokhon amra sum function call kori and amra ekhane amount some korbo 
        else:
            self.balance=self.request.user.account.balance
            # amader user jodi aggregate er kono kaj na kore taile user er j balance chilo seta take dekhay dibe 
        return queryset.distinct() #finally queryset gulo unique/distinct hote hobe 
    
    def get_context_data(self, **kwargs): # amader context data pass korte hoi form er moddhe tie nicher line ta thaktei hobe
        # ar amader account take pass kore dicchi jate kore 
        context=super().get_context_data(**kwargs)
        context.update({
            'account':self.request.user.account
        })
        return context
    
    
class PayLoanView(LoginRequiredMixin,View):
    def get(self,request,loan_id):
        loan=get_object_or_404(Transactions,id=loan_id) #jodi amader user er loan ta thake taile print korte parbo 
        print(loan)
        if loan.loan_approve: # jodi loan ta approved/ true hoi ...amader user backend theke approbe korbe
            user_account=loan.account # jodi loan approve hoye thake taile amra 1st e user er account take capture korlam 
               #Reduce the loan amount from the users balance
            if loan.amount<user_account.balance: # jodi loan er amount ta user er balance theke kom hoi taile 
                user_account.balance-=loan.amount # amra balance theke amount ta kete nilam 
                loan.balance_after_transaction=user_account.balance # erpor transaction ta ke update korchi 
                # balance_after_transaction er kaj oi hocche amader transaction howar age ba pore ja thakbe seta track rakha 
                user_account.save()
                loan.loan_approve=True # erpor save kore loan take approve korlam 
                loan.transaction_type=LOAN_PAID #er por transaction type loan theke setake loan_paid type dekhalam
                loan.save()
                return redirect('loan_list') # finallly loan list name ekta template thake sekahne redirect kore dibo 
            else: # jodi loan amount user er balance theke beshi taile ekta message show korbo 
                messages.error(
            self.request,
            f'Loan amount is greater than available balance'
        )
        return redirect('loan_list')
            
            
            
class LoanListView(LoginRequiredMixin,ListView): 
    model=Transactions
    template_name='transactions/loan_request.html'
    context_object_name='loans' # loan list ta ei loans context er moddhe thakbe 
    def get_queryset(self): # get query set theke filter korlam jodi transaction type=3 hoi taile
        # taile amader sei queryset k return korbo
        user_account=self.request.user.account
        queryset=Transactions.objects.filter(account=user_account,transaction_type=3)
        print(queryset)
        return queryset