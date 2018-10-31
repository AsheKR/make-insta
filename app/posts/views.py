import re

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from posts.forms import PostCreate, CommentCreate
from posts.models import Post, PostLike


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


def tag_form_search(request):
    keyword = request.GET.get('search_keyword')
    if keyword:
        sub_keyword = re.sub(r'#|\s+', '', keyword)
        return redirect('tag_search', sub_keyword)
    else:
        return redirect('posts:post_list')


def tag_search(request, tag_name):
    posts = Post.objects.filter(comment__hash_tag__tag_name=tag_name).distinct()

    context = {
        'posts': posts
    }
    return render(request, 'posts/post_list.html', context)


def post_like_toggle(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    post.post_like_toggle(request.user)

    url = reverse('posts:post_list')

    return redirect(url + f'#post-{post_pk}')


def my_posts(request):
    posts = Post.objects.filter(author=request.user)

    if not posts:
        messages.warning(request, '작성한 포스트가 없습니다..')
        return redirect('members:profile')

    context = {
        'posts': posts
    }

    return render(request, 'posts/post_list.html', context)