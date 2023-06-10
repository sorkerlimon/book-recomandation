from django.forms import ModelForm,CheckboxInput
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from dataclasses import fields
from .models import *

from django.forms.widgets import DateInput, FileInput

class CreateUserForm(UserCreationForm):
    phone = forms.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

   


    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists.")
        return email

    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.phone = self.cleaned_data['phone']
        if commit:
            user.save()
        return user


             
            
class DateInput(forms.DateInput):
    input_type = 'date'

class ProfleForm(ModelForm):
    class Meta:
        model = user_profile
        fields = ['name', 'dob','email']
        # exclude = ['user','u_user','has_used_secret_key','agreement_1','agreement_2','comment','license']
        labels = {
            'name':'Full Name',
            'email': 'Contact Email',
            'dob': 'Date of Birth',

            }
        # widgets = {'dob': DateInput(),
        #            'profile_pic': FileInput(attrs={'class': 'form-control', 'input_type': 'file'})
        #            }
        
        
    def __init__(self, *args, **kwargs):
        super(ProfleForm,self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        # self.fields['license'].widget = CheckboxInput(attrs={'class': 'form-check-input'})


