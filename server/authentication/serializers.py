from rest_framework import serializers

from .models import OneTimePassword, User

from tokenize import TokenError

from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_str, smart_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken, Token

from .utils import send_normal_email, validate_password_strength


class UserRegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(min_length=8, write_only=True)
    confirm_password=serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model=User
        fields=['email', 'name', 'password', 'confirm_password']
    
    def validate(self, attrs):
        password= attrs.get('password', '')
        confirm_password= attrs.get('confirm_password', '')

        validation_result = validate_password_strength(password, confirm_password)

        if not validation_result["is_password_strength_valid"]:
             raise serializers.ValidationError(validation_result["error_message"])
        
        
        return attrs
    
    def create(self, validated_data):
        user=User.objects.create_user(
            email=validated_data['email'],
            name=validated_data.get('name'),
            password=validated_data.get('password')
        )

        return user

class UserVerifyEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model=OneTimePassword
        fields=['code']

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    password=serializers.CharField(min_length=8, write_only=True)
    name = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model=User
        fields=['email', 'password', 'name', 'access_token', 'refresh_token']
    
    def validate(self, attrs):
        email=attrs.get('email')
        password=attrs.get('password')

        request=self.context.get('request')

        user=authenticate(request, email=email, password=password)

        if not user:
            raise AuthenticationFailed('Usuário ou senha inválidos!')
        if not user.have_email_verified:
            raise AuthenticationFailed("O e-mail não é verificado!")
        
        user_tokens=user.tokens()

        return {
            'email': user.email,
            'name': user.name,
            'access_token': str(user_tokens.get('access')),
            'refresh_token': str(user_tokens.get('refresh'))
        }

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields=['email']
    
    def validate(self, attrs):
        if User.objects.filter(email=attrs.get('email')).exists():
            user=User.objects.get(email=attrs.get('email'))

            uidb64=urlsafe_base64_encode(smart_bytes(user.id))
            token=PasswordResetTokenGenerator().make_token(user)

            request=self.context.get('request')

            site_domain='localhost:8080'
            relative_link=reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            abslink=f"http://{site_domain}{relative_link}"

            email_body=f"Olá! \n Uma redefinição de senha foi solicitada para sua conta.\n Clique no link abaixo para redefinir sua senha. \n {abslink}"
            data={
                'email_body': email_body,
                'email_subject': 'Redefinir sua senha',
                'to_email': user.email
            }
            send_normal_email(data)

        return super().validate(attrs)

class SetNewPasswordSerializer(serializers.Serializer):
    password=serializers.CharField(min_length=8, write_only=True)
    confirm_password=serializers.CharField(min_length=8, write_only=True)
    uidb64=serializers.CharField(write_only=True)
    token=serializers.CharField(write_only=True)

    class Meta:
        fields=['password', 'confirm_password', 'uidb64', 'token']
    
    def validate(self, attrs):
        try:
            token=attrs.get('token')
            uidb64=attrs.get('uidb64')
            password=attrs.get('password')
            confirm_password=attrs.get('confirm_password')

            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('O link de redefinição é inválido ou expirou', 401)
            
            validation_result = validate_password_strength(password, confirm_password)

            if not validation_result["is_password_strength_valid"]:
                raise AuthenticationFailed(validation_result["error_message"])
            
            user.set_password(password)
            user.save()

            return user
        except Exception as e:
            raise AuthenticationFailed(e, 401)

class LogoutUserSerializer(serializers.Serializer):
    refresh_token=serializers.CharField()

    default_error_messages={
        'bad_token': ('Token é inválido ou expirou!')
    }

    def validate(self, attrs):
        self.token=attrs.get('refresh_token')

        return attrs
    
    def save(self, **kwargs):
        try:
            token=RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail('bad_token')