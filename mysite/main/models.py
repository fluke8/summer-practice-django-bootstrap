from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100,  unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    id = models.IntegerField(null=False, primary_key=True)
    name = models.CharField(max_length=20)
    description = models.TextField()
    tags = models.CharField(max_length=40, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    img = models.ImageField(null=True, blank=True, upload_to="img/")
    views = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    ingredients = models.ManyToManyField(Ingredient)

    def __str__(self):
        return self.name

    def total_likes(self):
        return self.likes.count()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_images', blank=True)