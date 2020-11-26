import uuid
from datetime import date

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

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'date_of_birth']

    def __str__(self):
        return self.email

    @property
    def age(self):
        today = date.today()
        birth = self.date_of_birth
        return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))


class UnemployedUserMore(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True,
                                related_name='unemployed_user_more',
                                limit_choices_to={'role': User.Roles.UNEMPLOYED})
    insurance_company = models.ForeignKey('insurance_companies.InsuranceCompany', on_delete=models.CASCADE,
                                          related_name='clients')
    family_member_employee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                               related_name='family_members', null=True,
                                               limit_choices_to={'role': User.Roles.EMPLOYED})


class EmployedUserMore(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True,
                                related_name='employed_user_more',
                                limit_choices_to={'role': User.Roles.EMPLOYED})
    job = models.CharField(_('job'), max_length=50, blank=True)
    employer_company = models.ForeignKey('employer_companies.EmployerCompany', on_delete=models.CASCADE,
                                         related_name='employees', null=True)


class EmployerCompanyRepresentativeMore(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True,
                                related_name='employer_company_representative_more',
                                limit_choices_to={'role': User.Roles.EMPLOYER_COMPANY_REPRESENTATIVE})
    employer_company = models.OneToOneField('employer_companies.EmployerCompany', on_delete=models.CASCADE,
                                            related_name='employer_company_representative', null=True)


class UnemployedUser(User):
    base_role = User.Roles.UNEMPLOYED

    @property
    def more(self):
        return self.unemployed_user_more

    class Meta:
        proxy = True


class EmployedUser(User):
    base_role = User.Roles.EMPLOYED

    @property
    def more(self):
        return self.employed_user_more

    class Meta:
        proxy = True


class EmployerCompanyRepresentative(User):
    base_role = User.Roles.EMPLOYER_COMPANY_REPRESENTATIVE

    @property
    def more(self):
        return self.employer_company_representative_more

    class Meta:
        proxy = True


class Measurement(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4, editable=False)
    sdnn = models.PositiveIntegerField(_('sdnn'))
    sdann = models.PositiveIntegerField(_('sdann'))
    rmssd = models.PositiveIntegerField(_('rmssd'))
    start = models.DateTimeField(_('start'))
    end = models.DateTimeField(_('end'))

    class Meta:
        ordering = ['-end', 'start']


class InsurancePrice(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='insurance_prices')
    price = models.PositiveIntegerField(_('insurance price'))
    measurement = models.OneToOneField('Measurement', on_delete=models.CASCADE,  related_name='insurance_price')
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        ordering = ['-created']

