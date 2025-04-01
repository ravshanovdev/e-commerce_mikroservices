from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=13)
    email = models.EmailField(unique=True, blank=False, null=False)

    def __str__(self):
        return f"username: {self.username}---phone: {self.phone}---email: {self.email}"

