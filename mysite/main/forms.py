from .models import *
from django.forms import ModelForm, TextInput, Textarea, SelectMultiple, Select
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
    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    ingredients = forms.ModelMultipleChoiceField(queryset=Ingredient.objects.all(),
                                                 widget=forms.SelectMultiple(attrs={'class': 'form-control'}))

    new_ingredients = forms.CharField(label='Новые ингредиенты', required=False)

    class Meta:
        model = Recipe
        fields = ['name', 'description', 'img', 'category', 'ingredients', 'new_ingredients']

    def save(self, commit=True):
        new_ingredients_names = self.cleaned_data.get('new_ingredients')
        if new_ingredients_names:
            ingredient_names = [name.strip() for name in new_ingredients_names.split(',')]
            for name in ingredient_names:
                ingredient, created = Ingredient.objects.get_or_create(name=name)
                self.cleaned_data['ingredients'] = list(self.cleaned_data['ingredients']) + [ingredient]
        return super().save(commit=commit)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_ingredients'].widget.attrs.update({'class': 'form-control'})