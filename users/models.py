import uuid

from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db import models

from .managers import UserManager


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
                                         related_name='employees', related_query_name='employees',
                                         null=True)
    insurance_company = models.ForeignKey('insurance_companies.InsuranceCompany', on_delete=models.CASCADE,
                                          related_name='clients', related_query_name='clients',
                                          null=True)

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

    def save(self, *args, **kwargs):
        self.insurance_company = self.employer_company.insurance_company
        super().save(*args, **kwargs)

    class Meta:
        proxy = True


class EmployerCompanyRepresentative(User):
    base_role = User.Roles.EMPLOYER_COMPANY_REPRESENTATIVE

    class Meta:
        proxy = True
