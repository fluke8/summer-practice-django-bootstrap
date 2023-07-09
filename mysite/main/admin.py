from django.contrib import admin
from .models import *

admin.site.register(Recipe)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Ingredient)