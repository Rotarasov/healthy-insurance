import uuid

from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    class Roles(models.TextChoices):
        UNEMPLOYED = 'unemployed', _('Unemployed')
        EMPLOYED = 'employed', _('Employed')
        INSURANCE_COMPANY_REPRESENTATIVE = 'ic_representative', _('Insurance company representative')
        EMPLOYER_COMPANY_REPRESENTATIVE = 'ec_representative', _('Employer company representative')

    base_role = '__all__'

    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(_('email address'), max_length=255, unique=True)
    date_of_birth = models.DateField(_('date of birth'))
    role = models.CharField(_('role'), choices=Roles.choices, default=base_role, max_length=30)
    job = models.CharField(_('job'), max_length=50, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth']

    def __str__(self):
        return self.email


class UnemployedUser(User):
    base_role = User.Roles.UNEMPLOYED

    class Meta:
        proxy = True


class EmployedUser(User):
    base_role = User.Roles.EMPLOYED

    class Meta:
        proxy = True


class InsuranceCompanyRepresentative(User):
    base_role = User.Roles.INSURANCE_COMPANY_REPRESENTATIVE

    class Meta:
        proxy = True


class EmployerCompanyRepresentative(User):
    base_role = User.Roles.EMPLOYER_COMPANY_REPRESENTATIVE

    class Meta:
        proxy = True
