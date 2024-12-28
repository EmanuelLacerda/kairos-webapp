from .models import OneTimePassword, User
from .serializers import LoginSerializer, LogoutUserSerializer, PasswordResetRequestSerializer, SetNewPasswordSerializer, UserRegisterSerializer, UserVerifyEmailSerializer

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from .utils import send_code_to_user



class RegisterUserView(GenericAPIView):
    serializer_class=UserRegisterSerializer

    def post(self, request):
        user_data=request.data
        serializer=self.serializer_class(data=user_data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user=serializer.data

            send_code_to_user(user['email'])

            return Response({
                'data': user,
                'message': f'Oi, obrigado por criar sua conta no nosso aplicativo de calendário de eventos!! Espero que você consiga agendar muitos eventos por ele.'
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VerifyUserEmailView(GenericAPIView):
    serializer_class=UserVerifyEmailSerializer

    def post(self, request):
        otpcode=request.data.get('code')

        try:
            user_code_obj=OneTimePassword.objects.get(code=otpcode)
            user = user_code_obj.user

            if not user.have_email_verified:
                user.have_email_verified=True
                user.save()

                return Response({
                    'message': 'O e-mail foi verificado com sucesso'
                }, status=status.HTTP_200_OK)
            
            return Response({
                'message': 'Código inválido, usuário já verificado'
            }, status=status.HTTP_204_NO_CONTENT)
        except OneTimePassword.DoesNotExist:
            return Response({'message': 'Código não encontrado'}, status=status.HTTP_404_NOT_FOUND)

class LoginUserView(GenericAPIView):
    serializer_class=LoginSerializer

    def post(self, request):
        serializer=self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TestAuthenticationView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data={
            'msg': 'it works'
        }

        return Response(data, status=status.HTTP_200_OK)

class PasswordResetRequestView(GenericAPIView):
    serializer_class=PasswordResetRequestSerializer

    def post(self, request):
        serializer=self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        return Response({'message': "Um link foi enviado para seu e-mail para redefinir sua senha"}, status=status.HTTP_200_OK)

class PasswordResetConfirmView(GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            user_id=smart_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'message': 'Token é inválido ou expirou!'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success': True, 'message': 'Credenciais são válidas', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError:
            return Response({'message': 'Token é inválido ou expirou!'}, status=status.HTTP_401_UNAUTHORIZED)

class SetNewPasswordView(GenericAPIView):
    serializer_class=SetNewPasswordSerializer
    
    def patch(self, request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({'message': 'Sua senha foi redefinida com sucesso'}, status=status.HTTP_200_OK)

class LogoutUserView(GenericAPIView):
    serializer_class=LogoutUserSerializer
    permission_classes=[IsAuthenticated]

    def post(self, request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_200_OK)