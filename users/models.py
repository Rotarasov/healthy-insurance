import uuid

from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    class Roles(models.TextChoices):
        UNEMPLOYED = 'unemployed', _('Unemployed')
        EMPLOYED = 'employed', _('Employed')
        INSURANCE_COMPANY_MANAGER = 'ic_manager', _('Insurance company manager')
        EMPLOYER_COMPANY_MANAGER = 'ec_manager', _('Employer company manager')

    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(_('email address'), max_length=255, unique=True)
    date_of_birth = models.DateField(_('date of birth'))
    role = models.CharField(_('role'), choices=Roles.choices, default=Roles.UNEMPLOYED, max_length=30)
    job = models.CharField(_('job'), max_length=50, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth']

    def __str__(self):
        return self.email
