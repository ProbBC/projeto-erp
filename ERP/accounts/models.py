from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class CustomUser(AbstractUser):
    is_email_activated = models.BooleanField(_('active'), default=False)
