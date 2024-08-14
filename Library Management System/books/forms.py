from django import forms
from .models import Category,Comment
class categoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields='__all__'


class ComentForm(forms.ModelForm):
    class Meta:
        model=Comment
        exclude=['book','date']