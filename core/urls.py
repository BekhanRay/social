"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from apps import users
from apps.users.views import user_list, redirect_to_home
from core.settings import base

urlpatterns = [
    path('', redirect_to_home, name='redirect_to_home'),
    path('home/', user_list),
    path('admin/', admin.site.urls),
    path('user/', include('apps.users.urls')),
    path('forum/', include('apps.forum.urls')),
    path('chat/', include('apps.chat.urls')),
    path('home/', users.views.user_list, name='home'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if base.DEBUG:
    urlpatterns += static(base.MEDIA_URL, document_root=base.MEDIA_ROOT)


