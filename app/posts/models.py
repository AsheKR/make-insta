import re

from django.conf import settings
from django.db import models


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='작성자'
    )
    photo = models.ImageField(
        upload_to='posts/'
    )
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='PostLike',
        related_name='like_posts',
        related_query_name='like_post',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-pk']


class Comment(models.Model):
    TAG_REG_COMPILE = re.compile(r'#(\w+)')

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='작성자'
    )
    post = models.ForeignKey(
        'post',
        on_delete=models.CASCADE,
        verbose_name='포스트'
    )
    hash_tag = models.ManyToManyField(
        'HashTag',
        verbose_name='해시태그',
        blank=True,
    )
    content = models.CharField(
        max_length=150,
    )

    _html = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        def save_html():
            self._html = re.sub(self.TAG_REG_COMPILE, r"<a href='/explore/search/\1/'>#\1</a>", self.content)

        def save_tags():
            tags = [HashTag.objects.get_or_create(tag_name=name)[0] for name in re.findall(self.TAG_REG_COMPILE, self.content)]
            self.hash_tag.set(tags)

        save_html()
        super().save(*args, **kwargs)
        save_tags()

    @property
    def html(self):
        if self._html:
            return self._html


class HashTag(models.Model):
    tag_name = models.CharField(
        max_length=150,
        unique=True,
    )


class PostLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'post'), )
