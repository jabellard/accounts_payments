from django.dispatch import receiver
from pinax.eventlog.models import log
from allauth.account.signals import user_logged_in
from allauth.account.signals import user_logged_out


@receiver(user_logged_in)
def handle_user_logged_in(sender, **kwargs):
    log(
        user=kwargs.get('user'),
        action='USER_LOGGED_IN',
        extra={}
    )


# not triggered, investigate rest_auth & allauth views to find out why
@receiver(user_logged_out)
def handle_user_logged_in(sender, **kwargs):
    log(
        user=kwargs.get('user'),
        action='USER_LOGGED_OUT',
        extra={}
    )
