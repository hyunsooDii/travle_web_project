"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include # bookmark/urls 에 있는 파일 include
from . import views
from mysite.views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path('admin/', admin.site.urls), # 404 error 나올 때 봐야할 것



    path('country/', include('country.urls')),
    path('city/', include('city.urls')),
    path('food/', include('food.urls')),
    path('board/', include('board.urls')),
    path('detail_city/', include('detail_city.urls')),
    path('festival/', include('festival.urls')),

    # 회원 가입 및 처리
    path('auth/', include('django.contrib.auth.urls')),
    path('register/', register, name='register'),
    path('login/', login, name = 'login'),
    path('logout/', logout, name = 'logout'),
    path('tinymce/', include('tinymce.urls')),
    path('password_reset/', PasswordReset.as_view(), name="password_reset"),
    path('password_reset_done/', PasswordResetDone.as_view(), name="password_reset_done"),
    path('password_reset/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name="password_reset_confirm"),
    path('password_reset_complete/', PasswordResetComplete.as_view(), name="password_reset_complete"),
    # path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name="password_reset"),
    # path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name="password_reset_done"),
    # path('password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    # path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name="password_reset_complete"),
]
