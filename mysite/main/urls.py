from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('post/<int:pk>/add-to-favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('create', views.create, name='create'),
    path('post/<int:id>', views.post, name='post'),
    path('register/', views.register, name='register'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='main/logout.html'), name='logout'),
]
