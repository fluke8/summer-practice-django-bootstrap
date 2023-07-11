from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist


def index(request):
    search_query = request.GET.get('search', '')
    category = request.GET.get('category', '')
    ingredient = request.GET.get('ingredient', '')

    recipe = Recipe.objects.select_related('category').prefetch_related('ingredients').all()

    if search_query:
        recipe = recipe.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    if category:
        category_obj = get_object_or_404(Category, pk=category)
        recipe = recipe.filter(category=category_obj)

    if ingredient:
        recipe = recipe.filter(ingredients__name=ingredient)

    ingredients = Ingredient.objects.all()  # Получить все ингредиенты из базы данных

    context = {
        'title': 'Главная страница сайта',
        'recipe': recipe,
        'ingredients': ingredients,  # Передать ингредиенты в контекст шаблона
    }

    return render(request, 'main/index.html', context)


def about(request):
    return render(request, 'main/about.html')


@login_required
def create(request):
    error = ''
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            new_recipe = form.save(commit=False)
            new_recipe.author = request.user
            new_recipe.save()
            return redirect('home')
        else:
            error = 'error form'
    form = RecipeForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'main/create.html', context)


def post(request, id):
    post = get_object_or_404(Recipe, id=id)
    post.views += 1
    post.save()
    author_profile = post.author.userprofile
    favorite_posts = post.author.favorites.all()  # Посты, добавленные в избранное создателем поста
    context = {
        'post': post,
        'author_profile': author_profile,
        'favorite_posts': favorite_posts,
    }
    return render(request, 'main/post.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Создан аккаунт {username}!')

            # Аутентификация пользователя
            user = authenticate(request, username=username, password=form.cleaned_data['password1'])
            login(request, user)

            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'main/register.html', {'form': form})


@login_required
def add_to_favorites(request, pk):
    post = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        if request.user in post.favorites.all():
            post.favorites.remove(request.user)
        else:
            post.favorites.add(request.user)

    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def profile(request, username=None):
    if username is None:
        favorites = request.user.favorites.all()
    else:
        user = get_object_or_404(User, username=username)
        viewing_own_profile = request.user == user
        favorites = user.favorites.all()

    try:
        profile_form = UserProfileForm(instance=request.user.userprofile)
    except ObjectDoesNotExist:
        profile_form = UserProfileForm()

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Фото профиля успешно обновлено.')
            return redirect(reverse('profile', args=[request.user.username]))

    context = {
        'user': user,
        'viewing_own_profile': viewing_own_profile,
        'favorites': favorites,
        'profile_form': profile_form,
    }

    return render(request, 'main/profile.html', context)
