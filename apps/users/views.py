from datetime import date
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import UserFilterForm, UserChangeForm
from .models import Profile, CustomUser, Photo


def register(request):
    if request.method == 'POST':
        if CustomUser.objects.filter(email=request.POST['email']) is not None:
            user = CustomUser.objects.create_user(
                login=request.POST['login'],
                password=request.POST['password1'],
                email=request.POST['email'],
                nickname=request.POST['nickname'],
                birthdate=request.POST['birthdate'],
                confirmation_code=request.POST['confirmation_code'],
                gender=request.POST['gender'],
                country=request.POST['country'],
                region=request.POST['region'],
                city=request.POST['city'],
                user_agreement=bool([True if request.POST['user_agreement'] == 'on' else False]),
            )
            Profile.objects.create(user=user)
            if user:
                auth_login(request, user)
            else:
                return redirect('register')
        return redirect('profile')
    return render(request, 'register.html')


# def login_view(request):
#     if request.method == 'POST':
#         user = CustomUser.objects.get(login=request.POST['login'], password=request.POST['password'])
#         if user is not None:
#             auth_login(request, user)
#             return redirect('profile')  # Перенаправление на страницу профиля
#     else:
#         pass
#     return render(request, 'login.html')
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
        if request.method == 'POST':
            profile.general_info = request.POST['general_info']
            profile.personal_info = request.POST['personal_info']
            profile.education_profession = request.POST['education_profession']
            profile.habits_preferences = request.POST['habits_preferences']
            profile.updated_at = timezone.now()
            profile.save()
            # Optionally, you could add a message to indicate success
            return render(request, 'profile.html', {"form": profile, "message": "Profile updated successfully"})
        else:
            return render(request, 'profile.html', {"form": profile})
    except Profile.DoesNotExist:
        if request.method == 'POST':
            user = get_object_or_404(CustomUser, id=request.user.id)
            profile = Profile.objects.create(
                user=user,
                general_info=request.POST['general_info'],
                personal_info=request.POST['personal_info'],
                education_profession=request.POST['education_profession'],
                habits_preferences=request.POST['habits_preferences'],
                created_at=timezone.now(),
                updated_at=timezone.now()
            )
            profile.save()
            # Optionally, you could add a message to indicate success
            return render(request, 'profile.html', {"form": profile, "message": "Profile created successfully"})

    return render(request, 'profile.html')


def calculate_age(birthdate):
    today = date.today()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))


def user_list(request):
    form = UserFilterForm(request.GET or None)
    users = CustomUser.objects.exclude(pk=request.user.pk)

    if form.is_valid():
        max_age = form.cleaned_data.get('min_age')
        min_age = form.cleaned_data.get('max_age')
        region = form.cleaned_data.get('region')
        city = form.cleaned_data.get('city')
        country = form.cleaned_data.get('country')
        gender = form.cleaned_data.get('gender')
        is_online = form.cleaned_data.get('is_online')

        try:
            if min_age is not None:
                users = users.filter(birthdate__gte=date.today().replace(year=date.today().year - min_age))
            if max_age is not None:
                users = users.filter(birthdate__lte=date.today().replace(year=date.today().year - max_age - 1))
        except:
            pass
        if region:
            users = users.filter(region__icontains=region)
        if city:
            users = users.filter(city__icontains=city)
        if country:
            users = users.filter(country__icontains=country)
        if gender:
            users = users.filter(gender=gender)
        if is_online is not None:
            users = users.filter(is_online=is_online)

    return render(request, 'base.html', {'form': form, 'profiles': users})


def user_detail(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user_photos = Photo.objects.filter(user=user) or 'Нет фоток'
    profile = Profile.objects.get(user=user)
    return render(request, 'user_detail.html', {'user': user,
                                                'photos': user_photos,
                                                'profile': profile})


@login_required
def user_change(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST or None)
        user = CustomUser.objects.get(pk=request.user.pk)

        if form.is_valid():
            nickname = form.cleaned_data["nickname"]
            email = form.cleaned_data["email"]
            gender = form.cleaned_data["gender"]
            birthdate = form.cleaned_data["birthdate"]
            region = form.cleaned_data["region"]
            city = form.cleaned_data["city"]
            country = form.cleaned_data["country"]
            general_info = form.cleaned_data["general_info"]
            personal_info = form.cleaned_data["personal_info"]
            education_profession = form.cleaned_data["education_profession"]
            habits_preferences = form.cleaned_data["habits_preferences"]

            if nickname:
                user.nickname = nickname

            if email:
                user.email = email

            if gender:
                user.gender = gender

            if birthdate:
                user.birthdate = birthdate

            if region:
                user.region = region

            if city:
                user.city = city

            if country:
                user.country = country

            if general_info:
                user.profile.general_info = general_info

            if personal_info:
                user.profile.personal_info = personal_info

            if education_profession:
                user.profile.education_profession = education_profession

            if habits_preferences:
                user.profile.habits_preferences = habits_preferences

            user.save()
            messages.success(request, "Профиль успешно изменен!")
            return redirect("home")
        else:
            messages.error(request, "Введенные данные некорректны.")
    else:
        form = UserChangeForm()
    return render(request, "user_change.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect('register')
