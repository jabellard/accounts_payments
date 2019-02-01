from django.contrib import admin
from django.conf.urls import url
from django.urls import include
from django.urls import path
from django.views.generic import TemplateView
from .views import LoginView
from .views import LogoutView
from .views import PasswordChangeView
from .views import PasswordResetView
from .views import ResetPasswordView
from .views import PasswordResetConfirmView
from .views import RegisterView
from .views import VerifyEmailView
from .views import AccountEmailVerificationSentView

from .views import UserDetail
from .views import AccountConfirmView
from .views import GoogleLogin
from allauth.socialaccount.views import SignupView

urlpatterns = [
    # URLs that do not require a session or valid token
    url(r'^password/reset/$', PasswordResetView.as_view(),
        name='rest_password_reset'),
    path('reset_password/<uidb64>/<token>/', ResetPasswordView.as_view(),
         name='password_reset_confirm'),  # for password reset view error
    url(r'^password/reset/confirm/$', PasswordResetConfirmView.as_view(),
        name='rest_password_reset_confirm'),
    url(r'^login/$', LoginView.as_view(), name='rest_login'),
    # URLs that require a user to be logged in with a valid session / token.
    url(r'^logout/$', LogoutView.as_view(), name='rest_logout'),
    url(r'^password/change/$', PasswordChangeView.as_view(),
        name='rest_password_change'),
]

urlpatterns += [
    url(r'^oauth/google/$', GoogleLogin.as_view(), name='oauth_google'),
    # to resolve url reversing problem at oauth/google
    url(r'^oauth/socialaccount_signup/$', SignupView.as_view(), name='socialaccount_signup'),
]

urlpatterns += [
    url(r'^register/$', RegisterView.as_view(), name='rest_register'),
    url(r'^register/verify_email/$', VerifyEmailView.as_view(), name='rest_verify_email'),
    # simply for resolving url reversing error
    url(r'^register/account_email_verification_sent/$',
        AccountEmailVerificationSentView.as_view(), name='account_email_verification_sent'),

    # This url is used by django-allauth and empty TemplateView is
    # defined just to allow reverse() call inside app, for example when email
    # with verification link is being sent, then it's required to render email
    # content.

    # account_confirm_email - You should override this view to handle it in
    # your API client somehow and then, send post to /verify-email/ endpoint
    # with proper key.
    # If you don't want to use API on that step, then just use ConfirmEmailView
    # view from:
    # django-allauth https://github.com/pennersr/django-allauth/blob/master/allauth/account/views.py
    url(r'^register/confirm_email/(?P<key>[-:\w]+)/$', AccountConfirmView.as_view(),
        name='account_confirm_email'),
]

urlpatterns += [
    url(r'^current_user/$', UserDetail.as_view(), name='user_detail'),
    url(r'^current_user/membership/', include('apps.payments.urls')),
]

"""
# might be useful for solving url reserving problems
urlpatterns += [
    url(r'^rest_auth_', include('rest_auth.urls')),
    url(r'^all_auth_', include('allauth.urls')),
]
"""
