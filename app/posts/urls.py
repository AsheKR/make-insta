from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('my_posts/', views.my_posts, name='my_posts'),
    path('create/', views.post_create, name='post_create'),
    path('comment/<int:post_pk>', views.comment_create, name='comment_create'),
    path('like/<int:post_pk>', views.post_like_toggle, name='post_like_toggle')
]