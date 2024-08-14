from django.shortcuts import render,redirect
from . import forms
from django.views.generic import FormView
# Create your views here.
from . import forms
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

def register(request):
    if request.method=='POST':
        register_form=forms.regirtrationForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request,'account created succesfully')
    else:
        register_form=forms.regirtrationForm()
    return render(request,'register.html',{'form':register_form,'type':'register'})


def userlogin(request):
    if request.method=='POST':
        login_form=AuthenticationForm(request,request.POST)
        if login_form.is_valid():
            user_name=login_form.cleaned_data['username']
            user_pass=login_form.cleaned_data['password']
            user=authenticate(username=user_name,password=user_pass)
            if user is not None:
                messages.success(request,f'login succesfully')
                login(request,user)
                return redirect('homepage')
            else:
                messages.info(request,f'sorrry your submited information is incorrect')
                return redirect('register')
    else :
        login_form=AuthenticationForm()
    return render(request,'register.html',{'form':login_form,'type':'login'})

def user_logout(request):
    logout(request)
    return redirect('login')

# def profile(request):
#     data=User.objects.all()
#     return render(request,'profile.html',{'data':data})

def profile(request):
    user=request.user
    return render(request,'profile.html',{'user':user})


class UserAccountRegistrationView(FormView):
    template_name='accountRegister.html'
    form_class=forms.UserAccountRegistrationForm
    success_url=reverse_lazy('homepage')
    
    def form_valid(self,form):
        print('in account form valid')
        user=form.save()
        login(self.request,user)
        return super().form_valid(form) # form_valid function call hobhe jodi sohb thik thake