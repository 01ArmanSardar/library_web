from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Transaction
from .forms import DepositForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Sum
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string
# Create your views here.


def Transaction_mail(user,template,subject,amount):
        message=render_to_string(template,{
            'user':user,
            'amount':amount,
        })
        print(user.email)
        send_email=EmailMultiAlternatives(subject,'',to=[user.email])
        send_email.attach_alternative(message,'text/html')
        send_email.send()


        
class TransactionCreateMixin(LoginRequiredMixin,CreateView):
    template_name='transaction_form.html'
    model=Transaction
    # title=''
    success_url=reverse_lazy('homepage')

    def get_form_kwargs(self):
        kwargs=super().get_form_kwargs()
        kwargs.update(
            {
                'acount':self.request.user.account,
            }
        )
        return kwargs
    # def get_context_data(self,**kwargs):
    #     context=super().get_context_data(**kwargs)
    #     context.update(
    #         {
    #           'title'  :self.title
    #         }
    #     )
    #     return context

class DepositMoneyView(TransactionCreateMixin):
    form_class=DepositForm

    
    def form_valid(self,form):
        amount=form.cleaned_data.get('amount')
        account=self.request.user.account
        account.balance+=amount#user er kaceh ache 500 taka ,ami deposit korlam 1000 tk taile total balance hocche 1500
        account.save(
            update_fields=['balance']
        )
        # messages.success(self.request,f'{amount} was deposited to your account')

        # mail_subject="Deposite Message"
        # message=render_to_string('deposit_email.html',{
        #     'user':self.request.user,
        #     'amount':amount,
        # })
        # to_email=self.request.user.email
        # send_email=EmailMultiAlternatives(mail_subject,'',to=[to_email])
        # send_email.attach_alternative(message,'text/html')
        # send_email.send()

        Transaction_mail(self.request.user,'deposit_email.html',"Deposit Message",amount)
        return super().form_valid(form)
    

     