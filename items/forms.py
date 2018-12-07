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
        fields = ['username', 'email', 'password']

class Issued(forms.ModelForm):

    class Meta:
        model = Issued
        fields = ['box', 'quantity_issued', 'issue_or_use']

class ReturnIssue(forms.ModelForm):

    class Meta:
        model = Issued
        fields = ['return_number']

'''class DiscussionFormIndex(forms.ModelForm):
    #this class has a field for subject as subject.id cannot be imported.
    class Meta:
        model = Discussion
        fields = ['subject', 'question', 'title', 'picture', 'anonymous']

    #this function makes adding picture optional
    def __init__(self, *args, **kwargs):
        # credits: function used from stackoverflow
        super(DiscussionFormIndex, self).__init__(*args, **kwargs)
        self.fields['picture'].required = False'''
