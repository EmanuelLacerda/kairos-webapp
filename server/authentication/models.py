from django.db import models

from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255,verbose_name=_("Nome"))
    email = models.EmailField(max_length=255, unique=True, verbose_name=_("Endereço de e-mail"))
    is_superuser= models.BooleanField(default=False)
    is_staff= models.BooleanField(default=False)
    have_email_verified= models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    USERNAME_FIELD="email"

    REQUIRED_FIELDS= ["name"]

    objects= UserManager()

    def __str__(self):
        return f"{self.name}"
    
    def tokens(self):
        refresh=RefreshToken.for_user(self)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

class OneTimePassword(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    code=models.CharField(max_length=6, unique=True)

    def __str__(self):
        return f'{self.user.name}-passcode'