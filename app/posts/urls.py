from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('create/', views.post_create, name='post_create'),
    path('comment/<int:post_pk>', views.comment_create, name='comment_create'),
    path('like/<int:post_pk>', views.post_like_toggle, name='post_like_toggle')
]