from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from posts.forms import PostCreate, CommentCreate
from posts.models import Post


def post_list(request):
    posts = Post.objects.all()
    form = CommentCreate()
    context = {
        'posts': posts,
        'comment_form': form,
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


@login_required
def comment_create(request, post_pk):
    if request.method == 'POST':
        form = CommentCreate(request.POST)

        if form.is_valid():
            form.save(author=request.user, post=post_pk)

    url = reverse('posts:post_list')

    return redirect(url + f'#post-{post_pk}')
