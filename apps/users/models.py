
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .managers import UserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):

    GENDER_CHOICES = [
        ('мужской', 'Мужской'),
        ('женский', 'Женский'),
    ]

    login = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(max_length=100, unique=True)
    nickname = models.CharField(max_length=50)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=7, choices=GENDER_CHOICES, default='Другой')
    preffered_gender = models.CharField(max_length=7, choices=GENDER_CHOICES, default='Все')
    country = models.CharField(max_length=255, blank=True)
    region = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    user_agreement = models.BooleanField(default=False)
    confirmation_code = models.CharField(max_length=50, null=True, blank=True)
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

    @property
    def get_age(self):
        if len(str(self.age)) == 1 \
                and self.age == 1 \
                or str(self.age)[-1] == '1' \
                and self.age not in (11, 12, 13, 14,):
            return f'{self.age} год'
        if len(str(self.age)) == 1 \
                and 1 < self.age <= 4 \
                and self.age not in (11, 12, 13, 14,):
            return f'{self.age} года'
        if str(self.age)[-1] in ('2', '3', 4,) \
                and self.age not in (11, 12, 13, 14,):
            return f'{self.age} года'
        return f'{self.age} лет'


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    general_info = models.TextField(default='')
    personal_info = models.TextField(default='')
    education_profession = models.TextField(default='')
    habits_preferences = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.login


class Photo(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='photos')
    file_path = models.ImageField(upload_to='user_photos/', default='user_photos/default_user_photo.jpg')
    is_avatar = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def photo_url(self):
        return '%s%s' % (settings.HOST, self.photo.url) if self.photo else ''


@receiver(post_save, sender=CustomUser)
def create_default_avatar(sender, instance, created, **kwargs):
    if created and not instance.avatar_photo:
        default_photo = Photo.objects.create(user=instance, file_path='user_photos/default_user_photo.jpg', is_avatar=True)
        instance.avatar_photo = default_photo
        instance.save()


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


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='favorites', on_delete=models.CASCADE)
    favorite_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='favorited_by', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'favorite_user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} -> {self.favorite_user}"


