from rest_framework import serializers
from django.conf import settings
from .models import User
try:
    from rest_auth.serializers import LoginSerializer as _LoginSerializer
    from rest_auth.serializers import TokenSerializer as _TokenSerializer
    from rest_auth.serializers import JWTSerializer as _JWTSerializer
    from rest_auth.serializers import PasswordResetSerializer as _PasswordResetSerializer
    from rest_auth.serializers import PasswordResetConfirmSerializer as _PasswordResetConfirmSerializer
    from rest_auth.serializers import PasswordChangeSerializer as _PasswordChangeSerializer
    from rest_auth.registration.serializers import SocialAccountSerializer as _SocialAccountSerializer
    from rest_auth.registration.serializers import SocialLoginSerializer as _SocialLoginSerializer
    from rest_auth.registration.serializers import SocialConnectSerializer as _SocialConnectSerializer
    from rest_auth.registration.serializers import RegisterSerializer as _RegisterSerializer
    from rest_auth.registration.serializers import VerifyEmailSerializer as _VerifyEmailSerializer
except ImportError:
    raise ImportError("rest_auth needs to be added to INSTALLED_APPS.")

from django.contrib.auth import authenticate
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'user_id',
            'email',
            'first_name',
            'last_name',
            'date_joined',
            'is_active',
            'is_staff',
            'is_superuser',
            'last_login',
            'profile_picture',
        )
        read_only_fields = (
            'user_id',
            'email',
            'date_joined',
            'last_login',
        )


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'profile_picture',
        )


class UserDestroySerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ()


class LoginSerializer(_LoginSerializer):
    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')

        if 'allauth' in settings.INSTALLED_APPS:
            from allauth.account import app_settings
            # Authentication through email
            if app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.EMAIL:
                if email and password:
                    user = authenticate(email=email, password=password)
                else:
                    msg = _('Must include "email" and "password".')
                    raise exceptions.ValidationError(msg)
            # Authentication through username
            elif app_settings.AUTHENTICATION_METHOD == app_settings.AuthenticationMethod.USERNAME:
                if username and password:
                    user = authenticate(username=username, password=password)
                else:
                    msg = _('Must include "username" and "password".')
                    raise exceptions.ValidationError(msg)
            # Authentication through either username or email
            else:
                if email and password:
                    user = authenticate(email=email, password=password)
                elif username and password:
                    user = authenticate(username=username, password=password)
                else:
                    msg = _('Must include either "username" or "email" and "password".')
                    raise exceptions.ValidationError(msg)

        elif username and password:
            user = authenticate(username=username, password=password)

        else:
            msg = _('Must include "username" and "password".')
            raise exceptions.ValidationError(msg)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        # If required, is the email verified?
        if 'rest_auth.registration' in settings.INSTALLED_APPS:
            from allauth.account import app_settings
            if app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY:
                email_address = user.emailaddress_set.get(email=user.email)
                if not email_address.verified:
                    # added to have registation email confrimation re-sent
                    email_address.send_confirmation(
                        request=self.context.get('request')
                    )
                    raise serializers.ValidationError('E-mail is not verified.')

        attrs['user'] = user
        return attrs


class TokenSerializer(_TokenSerializer):
    pass


class JWTSerializer(_JWTSerializer):
    pass


class PasswordResetSerializer(_PasswordResetSerializer):
    def save(self):
        request = self.context.get('request')
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'subject_template_name': 'registration/password_reset_subject.txt',
            'email_template_name': 'registration/password_reset_email.html',
            'request': request,
        }
        self.reset_form.save(**opts)


class PasswordResetConfirmSerializer(_PasswordResetConfirmSerializer):
    pass


class PasswordChangeSerializer(_PasswordChangeSerializer):
    pass


class SocialAccountSerializer(_SocialAccountSerializer):
    pass


class SocialLoginSerializer(_SocialLoginSerializer):
    pass


class SocialConnectSerializer(_SocialConnectSerializer):
    pass


class RegisterSerializer(_RegisterSerializer):
    pass


class VerifyEmailSerializer(_VerifyEmailSerializer):
    pass
