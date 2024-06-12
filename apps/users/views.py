from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, ProfileForm
from django.shortcuts import get_object_or_404

from .models import Profile


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Перенаправление на страницу входа после успешной регистрации
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('profile')  # Перенаправление на страницу профиля
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except:
        profile = None

    if request.method == 'POST':

        # profile = get_object_or_404(Profile, user=request.user)
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile.html', {'form': form})
