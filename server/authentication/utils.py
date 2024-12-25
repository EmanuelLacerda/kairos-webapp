import random

from django.core.mail import EmailMessage
from django.conf import settings
from re import search as regex_search

from .models import User, OneTimePassword


def validate_password_strength(password, confirm_password):
    regex_numbers = r'\d'
    regex_lowercase = r'[a-z]'
    regex_uppercase = r'[A-Z]'

    if not(regex_search(regex_numbers, password)):
        return {"is_password_strength_valid": False, "error_message": {"password": "A senha deve ter, pelo menos, um caractere numérico!"}}
    
    if not(regex_search(regex_lowercase, password)):
        return {"is_password_strength_valid": False, "error_message": {"password": "A senha deve ter, pelo menos, uma letra minúscula!"}}
    
    if not(regex_search(regex_uppercase, password)):
        return {"is_password_strength_valid": False, "error_message": {"password": "A senha deve ter, pelo menos, uma letra maiúscula!"}}

    # verificação se a senha tem, pelo menos, um caractere especial

    if password != confirm_password:
        return {"is_password_strength_valid": False, "error_message": {"confirm_password": "As senhas devem ser iguais!"}}
    
    return {"is_password_strength_valid": True}


def generateOtp():
    otp=""

    for i in range(6):
        otp += str(random.randint(1,9))
    
    return otp

def send_code_to_user(email):
    otp_code=generateOtp()

    Subject=f"Código de verificação de e-mail: {otp_code}"
    user=User.objects.get(email=email)
    email_body=f"Insira o código de 6 dígitos abaixo para realizar a verificação de seu e-mail: \n {otp_code}"
    from_email=settings.DEFAULT_FROM_EMAIL

    OneTimePassword.objects.create(user=user, code=otp_code)

    send_email=EmailMessage(subject=Subject, body=email_body, from_email=from_email, to=[email])
    send_email.send(fail_silently=True)

def send_normal_email(data):
    email=EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        from_email=settings.EMAIL_HOST_USER,
        to=[data['to_email']]
    )

    email.send()