from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import ProfileForm #, CustomUserCreationForm

from .models import Profile, CustomUser


def register(request):
    if request.method == 'POST':
        if CustomUser.objects.filter(email=request.POST['email']) is not None:
            CustomUser.objects.create_user(
                login=request.POST['login'],
                password = request.POST['password1'],
                email = request.POST['email'],
                birthdate = request.POST['birthdate'],
                confirmation_code = request.POST['confirmation_code'],
                gender = request.POST['gender'],
                country = request.POST['country'],
                region = request.POST['region'],
                city = request.POST['city'],
                user_agreement = bool([True if request.POST['user_agreement'] == 'on' else False]),
            )
        return redirect('login')
        # form.save()
        # form = CustomUserCreationForm(request.POST)
        # if form.is_valid():
        #     form.save()
        #     return redirect('login')  # Перенаправление на страницу входа после успешной регистрации
    # else:
    #     form = CustomUserCreationForm()
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
