from datetime import date

from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.checks import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import UserFilterForm
from .models import Profile, CustomUser, Photo


def register(request):
    if request.method == 'POST':
        if CustomUser.objects.filter(email=request.POST['email']) is not None:
            CustomUser.objects.create_user(
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
        return redirect('login')
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
        return render(request, 'profile.html', {"form": profile})
    except:
        pass

    if request.method == 'POST':
        user = CustomUser.objects.get(id=request.user.id)
        image = request.FILES.get('image') or None
        if image:
            if user.avatar_photo:
                user.avatar_photo.file_path = 'user_photos/' + image
                user.avatar_photo.save()
            else:
                photo = Photo.objects.create(user=user, file_path=image, is_avatar=True)
                user.avatar_photo = photo
            user.save()
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
        return redirect('home')
    return render(request, 'profile.html')


def calculate_age(birthdate):
    today = date.today()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))


def user_list(request):
    form = UserFilterForm(request.GET or None)
    users = CustomUser.objects.all()

    if form.is_valid():
        min_age = form.cleaned_data.get('min_age')
        max_age = form.cleaned_data.get('max_age')
        region = form.cleaned_data.get('region')
        city = form.cleaned_data.get('city')
        country = form.cleaned_data.get('country')
        gender = form.cleaned_data.get('gender')
        is_online = form.cleaned_data.get('is_online')

        if min_age is not None:
            users = [user for user in users if calculate_age(user.birthdate) >= min_age]
        if max_age is not None:
            users = [user for user in users if calculate_age(user.birthdate) <= max_age]
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