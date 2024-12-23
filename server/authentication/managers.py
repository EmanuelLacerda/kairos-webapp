from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _



class UserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("Por favor informe um endereço de e-mail válido!"))
    
    def create_user(self, email, name, password, **extra_fields):
        if email:
            email=self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("Um endereço de e-mail deve ser informado!"))
        
        if not name:
            raise ValueError(_("Um nome de usuário deve ser informado!"))
    
        user=self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, name, password, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("is_superuser deve ser true para usuários administradores"))
        
        user=self.create_user(
            email, name, password, **extra_fields
        )
        # user.save(using=self._db)
        return user