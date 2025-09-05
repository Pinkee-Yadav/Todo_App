from django import forms
from .models import Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
  email = forms.EmailField(required=True)
    


class Meta:
   model = User
   fields = ('username', 'email', 'password1', 'password2')


class TaskForm(forms.ModelForm):
  class Meta:
    model = Task
    fields = ['title', 'description', 'completed']
    widgets = {
      'title': forms.TextInput(attrs={'class':'form-control','placeholder':'Task title'}),
      'description': forms.Textarea(attrs={'class':'form-control','rows':3,'placeholder':'Describe task (optional)'}),
      'completed': forms.CheckboxInput(attrs={'class':'form-check-input'}),
    }