from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.utils import timezone

from .models import Profile, CustomUser


def register(request):
    if request.method == 'POST':
        if CustomUser.objects.filter(email=request.POST['email']) is not None:
            CustomUser.objects.create_user(
                login=request.POST['login'],
                password=request.POST['password1'],
                email=request.POST['email'],
                birthdate=request.POST['birthdate'],
                confirmation_code=request.POST['confirmation_code'],
                gender=request.POST['gender'],
                country=request.POST['country'],
                region=request.POST['region'],
                city=request.POST['city'],
                user_agreement=bool([True if request.POST['user_agreement'] == 'on' else False]),
            )
        return redirect('login')
    return render(request, 'register.html')


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
        return render(request, 'profile.html', {"form": profile})
    except:
        pass

    if request.method == 'POST':
        profile = Profile.objects.create(
            user=request.user,
            general_info=request.POST['general_info'],
            personal_info=request.POST['personal_info'],
            education_profession=request.POST['education_profession'],
            habits_preferences=request.POST['habits_preferences'],
            created_at=timezone.now(),
            updated_at=timezone.now()
        )
        profile.save()
    return render(request, 'profile.html')
