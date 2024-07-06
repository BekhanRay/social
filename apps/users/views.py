
from datetime import date
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from .forms import UserFilterForm, UserChangeForm
from .models import Profile, CustomUser, Photo, Favorite

current_path = None


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if email and not CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.create_user(
                login=request.POST['login'],
                password=request.POST['password'],
                email=request.POST['email'],
                nickname=request.POST['nickname'],
                age=request.POST['age'],
                confirmation_code=request.POST['confirmation_code'],
                gender=request.POST['gender'],
                preffered_gender=request.POST['preffered_gender'],
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
            if 'avatar' in request.FILES.keys():
                avatar = Photo.objects.get(user=request.user, is_avatar=True)
                avatar.file_path = request.FILES['avatar']
                avatar.is_avatar = True
                avatar.save()
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


def user_list(request):
    form = UserFilterForm(request.GET or None)
    users = CustomUser.objects.exclude(pk=request.user.pk)
    if not request.user.is_authenticated:
        return redirect('register')
    else:
        favorites = request.user.favorites.values_list('favorite_user', flat=True)
    match request.user.preffered_gender:
        case 'Мужской':
            users = CustomUser.objects.filter(gender='Мужской').exclude(pk=request.user.pk)
        case 'Женский':
            users = CustomUser.objects.filter(gender='Женский').exclude(pk=request.user.pk)
        case 'Все':
            users = CustomUser.objects.all().exclude(pk=request.user.pk)

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
                users = users.filter(age__lte=min_age)
            if max_age is not None:
                users = users.filter(age__gte=max_age)
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

    return render(request, 'base.html', {'form': form,
                                         'profiles': users,
                                         'favorites': favorites})


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
        if 'avatar' in request.FILES.keys():
            avatar = Photo.objects.get(user=user, is_avatar=True)
            avatar.file_path = request.FILES['avatar']
            avatar.is_avatar = True
            avatar.save()
        if form.is_valid():
            nickname = form.cleaned_data["nickname"]
            email = form.cleaned_data["email"]
            gender = form.cleaned_data["gender"]
            preffered_gender = form.cleaned_data["preffered_gender"]
            age = form.cleaned_data["age"]
            region = form.cleaned_data["region"]
            city = form.cleaned_data["city"]
            country = form.cleaned_data["country"]
            general_info = form.cleaned_data["general_info"]
            personal_info = form.cleaned_data["personal_info"]
            education_profession = form.cleaned_data["education_profession"]
            habits_preferences = form.cleaned_data["habits_preferences"]
            profile = user.profile
            if nickname:
                user.nickname = nickname

            if email:
                user.email = email

            if gender:
                user.gender = gender

            if preffered_gender:
                user.preffered_gender =preffered_gender

            if age:
                user.age = age

            if region:
                user.region = region

            if city:
                user.city = city

            if country:
                user.country = country

            if general_info:
                profile.general_info = general_info

            if personal_info:
                profile.personal_info = personal_info

            if education_profession:
                profile.education_profession = education_profession

            if habits_preferences:
                profile.habits_preferences = habits_preferences

            user.save()
            profile.save()

            return redirect(reverse("user_detail", args=[request.user.id]))
    else:
        form = UserChangeForm()
    return render(request, "user_change.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect('register')


@login_required
def add_favorite(request, user_id):
    favorite_user = get_object_or_404(CustomUser, id=user_id)
    Favorite.objects.get_or_create(user=request.user, favorite_user=favorite_user)
    return JsonResponse({'status': 'ok'})


@login_required
def remove_favorite(request, user_id):
    favorite_user = get_object_or_404(CustomUser, id=user_id)
    favorite = get_object_or_404(Favorite, user=request.user, favorite_user=favorite_user)
    favorite.delete()
    return JsonResponse({'status': 'ok'})


@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('favorite_user')
    return render(request, 'favorite_list.html', {'favorites': favorites})


@login_required
def chat_bridge(request, username):
    # Perform any intermediate logic here, if needed
    user = get_object_or_404(CustomUser, login=username)

    # Redirect to the chat creation view
    response = redirect('create_chat', username=username)
    response.path = reverse('create_chat', args=[username])

    return response


def user_agreement(request):
    return render(request, 'user_agreement.html')

