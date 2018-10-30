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