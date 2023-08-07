# rbac_app/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


class CustomUser(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('user', 'User'),
        ('viewer', 'Viewer'),
    )

    role = models.CharField(max_length=10, choices=ROLES)
    tokens = models.CharField(max_length=500, blank=True, null=True)

class API(models.Model):
    name = models.CharField(max_length=100)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class UserAPIAccess(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    api = models.ForeignKey(API, on_delete=models.CASCADE)
    tokens = models.JSONField(blank=True, null=True)


    def generate_token(self):
        refresh = RefreshToken.for_user(self)
        self.tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.api.name}"
