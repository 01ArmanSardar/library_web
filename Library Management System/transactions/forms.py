from django import forms
from .models import Transaction
from Core.models import UserBankAccount

class userBankAccountForm(forms.ModelForm):
    class Meta:
        model=UserBankAccount
        fields=['accountNo']
 
class TransactionForm(forms.ModelForm):
    class Meta:
        model=Transaction
        fields=['amount']

    def __init__(self,*args,**kwargs):
        self.account=kwargs.pop('acount')
        super().__init__(*args,**kwargs)
        # self.fields['transaction_type'].disabled=True #ei feild disable takbhe
        # self.fields['transaction_type'].widget=forms.HiddenInput() # user tekeh hide korah takbhe

    def save(self,commit=True):
        self.instance.account=self.account
        self.instance.balance_after_transaction=self.account.balance
        return super().save()
    


class DepositForm(TransactionForm):
    def clean_amount(self):
        min_deposit_amount=100
        Amount=self.cleaned_data.get('amount')#user er fill korah form theke amara amount field er value ke niye aslam
        if Amount<min_deposit_amount:
            raise forms.ValidationError(
                f'you need to deposit at least {min_deposit_amount}$'
            )
        return Amount