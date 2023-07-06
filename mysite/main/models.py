from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Recipe(models.Model):
    id = models.IntegerField(null=False, primary_key=True)
    name = models.CharField(max_length=20)
    description = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    img = models.ImageField(null=True, blank=True, upload_to="img/")
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)


    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='profile_images', blank=True)