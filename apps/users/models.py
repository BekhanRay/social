
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import UserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    login = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=100, unique=True)
    nickname = models.CharField(max_length=50)
    birthdate = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    country = models.CharField(max_length=255, blank=True)
    region = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    user_agreement = models.BooleanField(default=False)
    confirmation_code = models.CharField(max_length=50)
    avatar_photo = models.ForeignKey('Photo', null=True, blank=True, on_delete=models.SET_NULL,
                                     related_name='avatar_user')
    is_online = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'login'

    objects = UserManager()
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.login


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    general_info = models.TextField(blank=True, null=True)
    personal_info = models.TextField(blank=True, null=True)
    education_profession = models.TextField(blank=True, null=True)
    habits_preferences = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.login

class Photo(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='photos')
    file_path = models.CharField(max_length=255)
    is_avatar = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Video(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='videos')
    url = models.URLField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Forum(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='forums')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Action(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image_path = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserAction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    is_participating = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Search(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='searches')
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    min_age = models.IntegerField()
    max_age = models.IntegerField()
    country = models.CharField(max_length=50, blank=True, null=True)
    region = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    with_photo = models.BooleanField(default=False)
    with_video = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Statistics(models.Model):
    total_users = models.IntegerField(default=0)
    users_online = models.IntegerField(default=0)
    new_users = models.TextField()
    random_photos = models.TextField()
