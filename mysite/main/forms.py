from .models import *
from django.forms import ModelForm, TextInput, Textarea, SelectMultiple, Select
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Ingredient
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


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
        fields = ['name', 'description', 'img', 'category', 'ingredients']

        widgets = {
            'img': forms.ClearableFileInput(
                attrs={'class': 'clearablefileinput form-control-file', 'id': 'id_img', 'label': ''})
        }


    def save(self, commit=True):
        recipe = super().save(commit=commit)
        return recipe

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-10'
        self.helper.add_input(Submit('submit', 'Добавить', css_class='btn btn-danger'))