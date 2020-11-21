import uuid

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db import models

from .managers import UserManager
from healthy_insurance import settings


class User(AbstractUser):
    class Roles(models.TextChoices):
        UNEMPLOYED = 'unemployed', _('Unemployed')
        EMPLOYED = 'employed', _('Employed')
        EMPLOYER_COMPANY_REPRESENTATIVE = 'ec_representative', _('Employer company representative')

    base_role = '__all__'

    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(_('email address'), max_length=255, unique=True)
    date_of_birth = models.DateField(_('date of birth'))
    role = models.CharField(_('role'), choices=Roles.choices, max_length=30)
    job = models.CharField(_('job'), max_length=50, blank=True)
    employer_company = models.ForeignKey('employer_companies.EmployerCompany', on_delete=models.CASCADE,
                                         related_name='employees', null=True)
    insurance_company = models.ForeignKey('insurance_companies.InsuranceCompany', on_delete=models.CASCADE,
                                          related_name='clients', null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth']

    def __str__(self):
        return self.email


class UnemployedUser(User):
    base_role = User.Roles.UNEMPLOYED

    def clean(self):
        if self.job:
            raise ValidationError({'job': _('Unemployed user can not have a job')})

        if self.employer_company:
            raise ValidationError({'employer_company': _('Unemployed user can not have an employer')})

        if not self.insurance_company:
            raise ValidationError({'insurance_company': _('Unemployed user must have insurance company')})

    class Meta:
        proxy = True


class EmployedUser(User):
    base_role = User.Roles.EMPLOYED

    def clean(self):
        if not self.job:
            raise ValidationError({'job': _('Employed user must have a job')})

        if not self.employer_company:
            raise ValidationError({'employer_company': _('Employed user must have a employer')})

        if self.insurance_company != self.employer_company.insurance_company:
            raise ValidationError(
                {'insurance_company': _('Employee must have insurance company the same as his employer company')}
            )

    class Meta:
        proxy = True


class EmployerCompanyRepresentative(User):
    base_role = User.Roles.EMPLOYER_COMPANY_REPRESENTATIVE

    def clean(self):
        if self.job:
            raise ValidationError({'job': _('Employer company manager can not have a job')})

        if not self.employer_company:
            raise ValidationError(
                {'employer_company': _('Employer company representative must have a employer company')}
            )

        if self.insurance_company != self.employer_company.insurance_company:
            raise ValidationError(
                {'insurance_company': _(
                    'Employer company representative must have insurance company the same as his employer company'
                )}
            )

    class Meta:
        proxy = True


class Measurement(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='measurements')
    sdnn = models.PositiveIntegerField(_('sdnn'))
    sdann = models.PositiveIntegerField(_('sdann'))
    rmssd = models.PositiveIntegerField(_('rmssd'))
    start = models.DateTimeField(_('start'))
    end = models.DateTimeField(_('end'))

