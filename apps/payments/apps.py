from importlib import import_module

from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):

    name = 'apps.payments'

    def ready(self):
        # import_module('apps.payments.receivers')
