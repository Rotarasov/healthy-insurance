from typing import Iterable

from .models import EmployerCompany, EmployerCompanyCoveragePrice


def get_employer_company_coverage_prices(employer_company: EmployerCompany) -> Iterable[EmployerCompanyCoveragePrice]:
    employees_insurance_prices_pk = [str(employee.user.insurance_prices.latest('created').id)
                                     for employee in employer_company.employees.all()]
    return EmployerCompanyCoveragePrice.objects.filter(user_insurance_price__id__in=employees_insurance_prices_pk)

