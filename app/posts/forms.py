from django import forms
from django.shortcuts import get_object_or_404

from posts.models import Post, Comment


class CommentCreate(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'content'
        ]
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                }
            )
        }

    def save(self, *args, **kwargs):
        comment = super().save(commit=False)
        comment.author = kwargs.get('author')
        comment.post = get_object_or_404(Post, pk=kwargs.get('post'))
        comment.save()
        return comment


class PostCreate(forms.Form):
    photo = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'form-control-file'
            }
        )
    )
    comment = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    def save(self, **kwargs):
        post = Post.objects.create(
            photo=self.cleaned_data['photo'],
            author=kwargs.get('author'),
        )

        if self.cleaned_data.get('comment'):
            post.comment_set.create(
                author=kwargs.get('author'),
                content=self.cleaned_data['comment']
            )

        return post
