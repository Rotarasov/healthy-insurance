import uuid

from django.utils.translation import ugettext_lazy as _
from django.db import models


class EmployerCompany(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('name'), max_length=160, unique=True)
    industry = models.CharField(_('industry'), max_length=30)
    insurance_coverage = models.FloatField(_('insurance coverage'), max_length=1.0, default=0.72)
    max_family_members = models.PositiveIntegerField(_('max family members'), default=4)
    insurance_company = models.ForeignKey('insurance_companies.InsuranceCompany', on_delete=models.CASCADE,
                                          related_name='partner_companies', related_query_name='partner_companies')


class EmployerCompanyCoveragePrice(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4, editable=False)
    price = models.PositiveIntegerField(_('insurance price'))
    employer_company = models.ForeignKey('EmployerCompany', on_delete=models.CASCADE, related_name='coverage_prices')
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        ordering = ['-created']

