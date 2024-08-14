from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserBankAccount


# class  regirtrationForm(UserCreationForm):
#     first_name=forms.CharField(widget=forms.TextInput(attrs={'id':'required'}))
#     last_name=forms.CharField(widget=forms.TextInput(attrs={'id':'required'}))
#     class Meta:
#         model=User
#         fields=['username','first_name','last_name','email']
    
class UserAccountRegistrationForm(UserCreationForm):
    
    class Meta:
        model=User
        fields=['username','password1','password2','first_name','last_name','email']

    def save (self,commit=True):
        our_user =super().save(commit=False) #ami dataBase data Save korbho nah akhn
        if commit==True:
            our_user.save()
            print('in form save method')
            UserBankAccount.objects.create(
                user=our_user,
                accountNo=100000+our_user.id
            )
        return our_user
    
    def __init__ (self,*args,**kwargs): #
        super().__init__(*args,**kwargs) #parent tah keh inherit koechi 
        for field in self.fields: #ai liner er manhe hocceh ai form a joutGulah field ache shob Gula keh amra ak ak kore nibho
            # nicer line gulu teh amrah mulutoh form er jeh field gulu aceh seh gular style add korchi ,aghe toh frontend a tekeh add krtm but akhne backend teke korlam ar kih
            self.fields[field].widget.attrs.update({
                
                'class' : (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                ) 
            })