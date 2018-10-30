from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from posts.forms import PostCreate
from posts.models import Post


def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'posts/post_list.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostCreate(request.POST, request.FILES)

        if form.is_valid():
            form.save(author=request.user)
            return redirect('posts:post_list')
    else:
        form = PostCreate()

    context = {
        'form': form
    }

    return render(request, 'posts/post_create.html', context)
