from .models import *
from django.forms import ModelForm, TextInput, Textarea, SelectMultiple, Select
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Ingredient


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
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    ingredients = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all(),
                                                 widget=forms.SelectMultiple(attrs={'class': 'form-control'}))

    class Meta:
        model = Recipe
        fields = ['name', 'description', 'img', 'category', 'ingredients']

    def save(self, commit=True):
        recipe = super().save(commit=commit)
        return recipe

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)