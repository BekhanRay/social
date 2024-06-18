import random

from django.conf import settings
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.checks import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.utils import timezone

from .models import Profile, CustomUser


def generate_code():
    random.seed()
    return str(random.randint(10000,99999))


def register(request):
    if request.method == 'POST':
        if CustomUser.objects.filter(email=request.POST['email']) is not None:
            # message = generate_code()
            # send_mail('код подтверждения', message,
            #           settings.EMAIL_HOST_USER,
            #           [CustomUser.objects.get(email=request.POST['email'])],
            #           fail_silently=False)
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
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=login, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('profile')  # Перенаправление на страницу профиля
            else:
                messages.error(request, "Неверный логин или пароль.")
        else:
            messages.error(request, "Неверный логин или пароль.")
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
    # elif request.method == 'GET':
    #     return render(request, 'profile.html', {"form": Profile.objects.get(user=request.user)})
    return render(request, 'profile.html')


@login_required
def logout_view(request):
    auth_logout(request)
    return redirect('register')


def profile_detail(request):
    user = CustomUser.objects.get(id=request.user.id)
    profile = Profile.objects.get(user=user)
    return render(request, 'profile_detail.html', {'user': user, 'profile': profile})