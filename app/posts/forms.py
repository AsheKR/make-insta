from django import forms

from posts.models import Post


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