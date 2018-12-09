from django import forms
from django.contrib.auth.models import User
from .models import Box, Issued

#this file is for tweaking the default UserForm to remove useless fiels and add new forms.

class UserForm(forms.ModelForm):
    #this tells django is password is a password field
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        #user model already exists in django
        model = User
        #use only given fields and omit useless fields like DOB, first name etc.
        fields = ['username', 'password']

class IssuedForm(forms.ModelForm):

    class Meta:
        model = Issued
        fields = ['box', 'quantity_issued']

class LocationForm(forms.ModelForm):

    class Meta:
        model = Box
        fields = ['number', 'location']

class ReturnIssue(forms.ModelForm):

    class Meta:
        model = Issued
        fields = ['return_number']