import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _


class InsuranceCompany(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('name'), max_length=160, unique=True)
    individual_price = models.PositiveIntegerField(_('individual price'))
    family_price = models.PositiveIntegerField(_('family price'))
    company_sale = models.FloatField(_('company sale'), default=0.1)
    company_employees_num = models.PositiveIntegerField(_('company employees num'), default=100)


