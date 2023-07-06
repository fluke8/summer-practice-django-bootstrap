from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def index(request):
    search_query = request.GET.get('search', '')

    if search_query:
        recipe = Recipe.objects.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query) | Q(tags__icontains=search_query))
    else:
        recipe = Recipe.objects.all()

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
def profile(request):
    profile_form = UserProfileForm(data=request.POST)

    if profile_form.is_valid():
        profile = profile_form.save(commit=False)
        profile.user = request.user
        if 'photo' in request.FILES:
            profile.photo = request.FILES['photo']
    return render(request, 'main/profile.html')
