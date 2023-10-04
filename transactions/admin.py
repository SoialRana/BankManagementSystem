from django.contrib import admin

# from transactions.models import Transaction
from .models import Transactions
@admin.register(Transactions)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['account', 'amount', 'balance_after_transaction', 'transaction_type', 'loan_approve']
    
    def save_model(self, request, obj, form, change):
        obj.account.balance += obj.amount # amra jokhon loan approved kortechi tar sathe amader amount ta jog hoye jabe 
        obj.balance_after_transaction = obj.account.balance
        obj.account.save()
        super().save_model(request, obj, form, change)
