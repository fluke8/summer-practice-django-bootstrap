from .models import *
from django.forms import ModelForm, TextInput, Textarea
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('photo', )


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ["name", "description", "img", "tags"]
        labels = {
            'name': '',
            'description': '',
            'img': '',
            'tags': ''
        }
        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название'
            }),
            "description": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание'
            }),
            "tags": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите теги через запятую'
            })
        }