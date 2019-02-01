from importlib import import_module

from django.apps import AppConfig as BaseAppConfig


class AppConfig(BaseAppConfig):

    name = 'apps.accounts'

    def ready(self):
        # import_module('apps.accounts.receivers')
        #from apps.accounts.recievers import *
