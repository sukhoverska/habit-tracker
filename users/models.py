from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    avatar = models.ImageField(
        upload_to='avatars/',
        null=True,
        blank=True
    )
    timezone = models.CharField(
        max_length=50,
        default='Europe/Kyiv'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username