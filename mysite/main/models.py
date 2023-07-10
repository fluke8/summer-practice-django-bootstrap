from django.db import models
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=300,  unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    img = models.ImageField(null=True, blank=True, upload_to="img/")
    views = models.IntegerField(default=0)
    favorites = models.ManyToManyField(User, blank=True, related_name='favorites')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    ingredients = models.ManyToManyField(Ingredient)

    def __str__(self):
        return self.name

    def total_added_to_favorites(self):
        return self.favorites.count()

    def is_favorited_by(self, user):
        return user in self.favorites.all()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(default='default.jpg', upload_to='profile_images')

    def __str__(self):
        return f'{self.user.username} Profile'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()