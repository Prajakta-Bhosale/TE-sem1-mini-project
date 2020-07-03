from django.forms import ModelForm
from .models import *
from django import forms

class LoginForm(ModelForm):
    class Meta:
        model=LoginModel
        fields=['Mobile_No']

class OTPForm(ModelForm):
    class Meta:
        model=OTPModel
        fields=['Enter_OTP']


class EventForm(ModelForm):
    Budget = forms.FloatField(min_value=0.0)
    class Meta:
        model=EventModel
        fields=['EventName','SubEventName','EventDate','Budget','Description','NoOfParticipants','Outcomes']


class EditForm(ModelForm):
    class Meta:
        model=EditModel
        fields=['EventName','EventDate']

class SearchForm(ModelForm):
    class Meta:
        model=SearchModel
        fields=['EventName','EventDate']


class EventAnalyzeSearchForm(ModelForm):
    class Meta:
        model=AnalyzeSearchModel
        fields=['EventName']

class AnalyzeSearchForm(ModelForm):
    class Meta:
        model=AnalyzeSearchModel
        fields=['EventName','SubEventName']


class EmailForm(forms.ModelForm):
    email = forms.EmailField(max_length=200,widget=forms.TextInput(attrs={'class': "form-control",'id': "clientemail"}))
    message = forms.CharField( widget=forms.Textarea(attrs={'class': "form-control"}))
    subject = forms.CharField( widget=forms.TextInput(attrs={'class': "form-control"}))
    class Meta:
        model = Mails
        fields = ('email','subject','message','document',)
        