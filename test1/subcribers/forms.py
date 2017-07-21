from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Subscrpber
class AddressMixin(forms.ModelForm):
    CHOICES1 = [('1', '수신'), ('0', '거부')]
    class Meta:
        model=Subscrpber
        fields=('call_number','event1','event2','event3')
        widgets={
            'call_number': forms.TextInput(attrs={'class':'form-control'}),
            'event1': forms.TextInput(attrs={'class': 'form-control'}),
            'event2': forms.TextInput(attrs={'class':'form-control'}),
            'event3': forms.TextInput(attrs={'class': 'form-control'}),
        }
    email_check = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class': "with-gap"}), choices=CHOICES1)
class SubscrpberForm(AddressMixin,UserCreationForm):
    first_name=forms.CharField(
        required=True,widget=forms.TextInput(attrs={'class':'form-control'})
    )
    last_name=forms.CharField(
        required=True,widget=forms.TextInput(attrs={'class':'form-control'})
    )
    email=forms.EmailField(
        required=True,widget=forms.TextInput(attrs={'class':'form-control'})
    )
    username=forms.CharField(
        required=True,widget=forms.TextInput(attrs={'class':'form-control'})
    )
    password1=forms.CharField(
        required=True,widget=forms.TextInput(attrs={'class':'form-control','type':'password'})
    )
    password2=forms.CharField(
        required=True,widget=forms.TextInput(attrs={'class':'form-control','type':'password'})
    )


