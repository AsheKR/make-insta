from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    img_profile = models.ImageField(
        upload_to='users/',
        blank=True,
    )
    site = models.CharField(
        max_length=500,
        blank=True,
        null=True,
    )
    introduce = models.TextField(
        blank=True,
        null=True,
    )
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='FollowRelation',
    )

    @property
    def follower_list(self):
        return self.followers.all()

    @property
    def following_list(self):
        return User.objects.filter(to_user_relation__from_user=self)

    def follow_toggle(self, user):
        now_follow, created = FollowRelation.objects.get_or_create(to_user=user, from_user=self)
        if not created:
            now_follow.delete()
        return now_follow


class FollowRelation(models.Model):
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='to_user_relations',
        related_query_name='to_user_relation',
    )
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='from_user_relations',
        related_query_name='from_user_relation',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('to_user', 'from_user'),
        )