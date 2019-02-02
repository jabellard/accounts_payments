from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    pass


class User(AbstractUser):
    '''
    User model.
    '''

    user_id = models.AutoField(
        primary_key=True
    )
    email = models.EmailField(
        _('email address'),
        unique=True
    )
    profile_picture = models.ImageField(
        upload_to='image_uploads/',
        max_length=255,
        null=True,
        blank=True
    )

    def __str__(self):
        return '%s' % (self.username)

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
