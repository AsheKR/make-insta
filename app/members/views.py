from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from members.forms import LoginForm


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
        'form': form
    }

    return render(request, 'members/login.html', context)