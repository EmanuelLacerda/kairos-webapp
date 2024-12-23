from django.urls import path
from .views import LogoutUserView, PasswordResetConfirmView, PasswordResetRequestView, RegisterUserView, SetNewPasswordView, VerifyUserEmailView, LoginUserView, TestAuthenticationView

urlpatterns = [
    # register user endpoint
    path('register/', RegisterUserView.as_view(), name='register'),

    # verify e-mail of user endpoint
    path('verify-email/', VerifyUserEmailView.as_view(), name='verify'),

    # login and logout endpoints
    path('login/', LoginUserView.as_view(), name='login'),
    path('profile/', TestAuthenticationView.as_view(), name='granted'),
    path('logout/', LogoutUserView.as_view(), name='logout'),

    # change password endpoints
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('set-new-password/', SetNewPasswordView.as_view(), name='set-new-password'),
]