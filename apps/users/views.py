import io

from PIL import Image
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordChangeView, PasswordResetView
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .forms import UserFilterForm, UserChangeForm, UserPasswordChangeForm
from .models import Profile, CustomUser, Photo, Favorite, UserPromotion, Promotion
from .utils import send_verification_mail


@login_required
def promotion_list(request):
    promotions = Promotion.objects.filter(is_active=True)

    return render(request, 'promotion_list.html', {'promotions': promotions})


@login_required
def print_flyer(request, promotion_id):
    promotion = Promotion.objects.get(id=promotion_id, is_active=True)
    user_promotion = UserPromotion.objects.get_or_create(user=request.user, promotion=promotion, is_participating=True)

    flyer_path = promotion.flyer.path  # Ensure `flyer` is an ImageField in your model
    flyer_image = Image.open(flyer_path)

    # Convert the image to PDF
    pdf_buffer = io.BytesIO()
    flyer_image.convert('RGB').save(pdf_buffer, format='PDF')
    pdf_buffer.seek(0)

    # Set response as PDF file
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="flyer_{promotion.title}.pdf"'

    return response


# def register(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         if email and not CustomUser.objects.filter(email=email).exists():
#             user = CustomUser.objects.create_user(
#                 login=request.POST['login'],
#                 password=request.POST['password'],
#                 email=request.POST['email'],
#                 nickname=request.POST['nickname'],
#                 age=request.POST['age'],
#                 gender=request.POST['gender'],
#                 preffered_gender=request.POST['preffered_gender'],
#                 country=request.POST['country'],
#                 region=request.POST['region'],
#                 city=request.POST['city'],
#                 user_agreement=bool([True if request.POST['user_agreement'] == 'on' else False]),
#             )
#             Profile.objects.create(user=user)
#             if user:
#                 send_verification_mail(request.POST.get('email'))
#                 auth_login(request, user)
#             else:
#                 return redirect('register')
#         return redirect('profile')
#     return render(request, 'register.html')
@csrf_exempt
def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        code = request.POST.get('confirmation_code')
        if email and not CustomUser.objects.filter(email=email).exists():
            request.session['login'] = request.POST['login']
            request.session['password'] = request.POST['password']
            request.session['email'] = request.POST['email']
            request.session['nickname'] = request.POST['nickname']
            request.session['age'] = request.POST['age']
            request.session['gender'] = request.POST['gender']
            request.session['preffered_gender'] = request.POST['preffered_gender']
            request.session['country'] = request.POST['country']
            request.session['region'] = request.POST['region']
            request.session['city'] = request.POST['city']
            request.session['user_agreement'] = request.POST['user_agreement']
            request.session['confirmation_code'] = send_verification_mail(email)
            return render(request, 'code_confirm.html')
        if code:
            if code == request.session['confirmation_code']:
                user = CustomUser.objects.create_user(
                    login=request.session['login'],
                    password=request.session['password'],
                    email=request.session['email'],
                    nickname=request.session['nickname'],
                    age=request.session['age'],
                    gender=request.session['gender'],
                    preffered_gender=request.session['preffered_gender'],
                    country=request.session['country'],
                    region=request.session['region'],
                    city=request.session['city'],
                    user_agreement='user_agreement' in request.session,
                )
                Profile.objects.create(user=user)
                auth_login(request, user)
                return redirect('profile')
            else:
                messages.error(request, 'Неверный код подтверждения.')
                return render(request, 'code_confirm.html')
        else:
            messages.error(request, 'Почта неверна или уже существует.')
            return redirect('register')
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
        user_photos = Photo.objects.filter(user=request.user, is_avatar=False)
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
            return render(request, 'user_detail.html', {"profile": profile,
                                                        "photos": user_photos,
                                                        "message": "Profile updated successfully"})
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
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        favorites = request.user.favorites.values_list('favorite_user_id', flat=True)
    form = UserFilterForm(request.GET or None)
    users = CustomUser.objects.exclude(pk=request.user.pk)

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


@login_required
def delete_photo(request, photo_id):
    if photo_id:
        Photo.objects.get(user=request.user,
                          id=photo_id).delete()
    return redirect(reverse("user_detail", args=[request.user.id]))


def user_detail(request, user_id):
    if 'photo' in request.FILES.keys():
        photo = Photo.objects.create(user=request.user,
                                     file_path=request.FILES['photo'])
        photo.save()
    user = get_object_or_404(CustomUser, id=user_id)
    user_photos = Photo.objects.filter(user=user, is_avatar=False)
    profile = Profile.objects.get(user=user)
    favorites = Favorite.objects.filter(user=request.user).select_related('favorite_user')
    return render(request, 'user_detail.html', {'user': user,
                                                'photos': user_photos,
                                                'profile': profile,
                                                'favorites': favorites})

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
    return redirect('redirect_to_home')


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


def user_agreement(request):
    return render(request, 'user_agreement.html')


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("password_change_done")
    template_name = "password_change_form.html"


class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        if not CustomUser.objects.filter(email=email).exists():
            # Если email не найден в базе данных, верните ошибку
            form.add_error('email', 'Пользователь с таким email не найден')
            return self.form_invalid(form)
        # Если email найден, продолжайте с обычной обработкой
        return super().form_valid(form)


def redirect_to_home(request):
    return redirect('home')
