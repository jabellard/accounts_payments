from django.views.generic import TemplateView as _TemplateView
try:
    from rest_auth.views import LoginView as _LoginView
    from rest_auth.views import LogoutView as _LogoutView
    from rest_auth.views import PasswordChangeView as _PasswordChangeView
    from rest_auth.views import PasswordResetView as _PasswordResetView
    from rest_auth.views import PasswordResetConfirmView as _PasswordResetConfirmView
    from rest_auth.registration.views import RegisterView as _RegisterView
    from rest_auth.registration.views import VerifyEmailView as _VerifyEmailView
except ImportError:
    raise ImportError("rest_auth needs to be added to INSTALLED_APPS.")

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView


from django.shortcuts import render
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from .serializers import UserUpdateSerializer
from .serializers import UserDestroySerializer


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class TemplateView(_TemplateView):
    pass


class LoginView(_LoginView):
    pass


class LogoutView(_LogoutView):
    pass


class PasswordChangeView(_PasswordChangeView):
    pass


class PasswordResetView(_PasswordResetView):
    pass


class PasswordResetConfirmView(_PasswordResetConfirmView):
    pass


class ResetPasswordView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        return Response(
            {
                'detail': 'Not implemented. Use django.contrib.auth.views.PasswordResetConfirmView or redirect to a view on the API client (React app).'
            },
            status=status.HTTP_501_NOT_IMPLEMENTED
        )


class RegisterView(_RegisterView):
    pass


class VerifyEmailView(_VerifyEmailView):
    def get(self, request, *args, **kwargs):
        return Response(
            {
                'detail': 'Not implemented.'
            },
            status=status.HTTP_501_NOT_IMPLEMENTED
        )


class AccountConfirmView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        key = request.GET.get('key')
        return Response(
            {
                'detail': 'Not implemented. Should use allauth.account.views.ConfirmEmailView or redirect to a view on the API client (React app).'
            },
            status=status.HTTP_501_NOT_IMPLEMENTED
        )


class AccountEmailVerificationSentView(generics.RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        return Response(
            {
                'detail': 'Not implemented.'
            },
            status=status.HTTP_501_NOT_IMPLEMENTED
        )


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = None
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        self.serializer_class = UserSerializer
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return Response(
            {
                'detail': 'Not implemented. Use PATCH'
            },
            status=status.HTTP_501_NOT_IMPLEMENTED
        )

    def patch(self, request, *args, **kwargs):
        self.serializer_class = UserUpdateSerializer
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.serializer_class = UserDestroySerializer
        return self.destroy(request, *args, **kwargs)

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        """
        Adding this method since it is sometimes called when using
        django-rest-swagger
        https://github.com/Tivix/django-rest-auth/issues/275
        """
        return get_user_model().objects.none()
