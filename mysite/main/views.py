from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.http import require_http_methods

def index(request):
    search_query = request.GET.get('search', '')
    category = request.GET.get('category', '')
    ingredient = request.GET.get('ingredient', '')

    recipe = Recipe.objects.all()

    if search_query:
        recipe = recipe.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query) | Q(ingredients__name__icontains=search_query) | Q(category__name__icontains=search_query)
        )

    if category:
        recipe = recipe.filter(category=category)

    if ingredient:
        recipe = recipe.filter(ingredients=ingredient)

    return render(request, 'main/index.html', {'title': 'Главная страница сайта', 'recipe': recipe})


def about(request):
    return render(request, 'main/about.html')


def create(request):
    error = ''
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.author = request.user
            new_topic.tags = new_topic.tags.title()
            new_topic.save()
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
    post.views+=1
    post.save()
    context = {'post': post}
    return render(request, 'main/post.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():

            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Создан аккаунт {username}!')
            Profile(user=User.objects.get(username=form.cleaned_data['username']), ).save()
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'main/register.html', {'form': form})


@login_required
def like(request, pk):
    post = get_object_or_404(Recipe, pk=pk)
    if request.method == 'POST':
        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            post.likes.add(request.user)
        else:
            post.likes.remove(request.user)

    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def profile(request):
    profile_form = UserProfileForm(data=request.POST)

    if profile_form.is_valid():
        profile = profile_form.save(commit=False)
        profile.user = request.user
        if 'photo' in request.FILES:
            profile.photo = request.FILES['photo']
    return render(request, 'main/profile.html')
