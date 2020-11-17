import uuid

from django.utils.translation import ugettext_lazy as _
from django.db import models


class EmployerCompany(models.Model):
    id = models.UUIDField(_('id'), primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_('name'), max_length=160, unique=True)
    industry = models.CharField(_('industry'), max_length=30)
    insurance_coverage = models.FloatField(_('insurance coverage'), max_length=1.0, default=0.72)
    max_family_members = models.PositiveIntegerField(_('max family members'), default=4)

