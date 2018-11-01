import imghdr
import json

import requests
from django.conf import settings
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from members.forms import LoginForm, ProfileForm, SignupForm

User = get_user_model()


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            login(request, form.user)

            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            return redirect('posts:post_list')
    else:
        form = LoginForm()

    context = {
        'form': form,
        'FACEBOOK_APP_ID': settings.FACEBOOK_APP_ID
    }

    return render(request, 'members/login.html', context)


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('posts:post_list')


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()

    # 다시 불러와야 이미지에 대한 정보를 담는다.
    form = ProfileForm(instance=request.user)

    context = {
        'form': form
    }

    return render(request, 'members/profile.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('posts:post_list')
    else:
        form = SignupForm()
    context = {
        'form': form
    }
    return render(request, 'members/signup.html', context)


def facebook_login(request):
    user = authenticate(request, facebook_request_token=request.GET.get('code'))

    if user:
        login(request, user)
        return redirect('posts:post_list')

    return redirect('members:login_view')


def follow_toggle(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    request.user.follow_toggle(user)
    return redirect('members:profile')
