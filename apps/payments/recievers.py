from django.dispatch import receiver
from pinax.eventlog.models import log
from pinax.stripe.actions import customers
from pinax.stripe.signals import WEBHOOK_SIGNALS
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.db.models.signals import post_delete
from django.conf import settings
from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import social_account_added


@receiver(user_signed_up)
def handle_user_signed_up(sender, **kwargs):
    log(
        user=kwargs.get('user'),
        action='USER_SIGNED_UP',
        extra={}
    )
    customers.create(kwargs.get('user'))


@receiver(pre_delete, sender=settings.AUTH_USER_MODEL)
def handle_user_pre_delete(sender, **kwargs):
    user = kwargs.get('instance')
    customer = customers.get_customer_for_user(user=user)
    if customer:
        customers.purge(customer=customer)


'''
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def handle_user_created(sender, instance, created, **kwargs):
    if created:
        print('-----------------------------------------------')
        print('--------------user created--------------------')
        print('-----------------------------------------------')
        log(
            user=instance,
            action='USER_CREATED',
            extra={}
        )
        customers.create(instance)

@receiver(WEBHOOK_SIGNALS['customer.created'])
def handle_customer_created(sender, event, **kwargs):
    print('-----------------------------------------------')
    print(event)
    print('-----------------------------------------------')
'''
