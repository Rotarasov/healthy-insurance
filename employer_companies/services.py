from typing import Iterable

from django.contrib.auth import get_user_model

from users.models import InsurancePrice
from users.services import get_latest_user_insurance_price
from .models import EmployerCompany, EmployerCompanyCoveragePrice, EmployerCompanyPrice


User = get_user_model()


def get_employer_company_coverage_prices(employer_company: EmployerCompany) -> Iterable[EmployerCompanyCoveragePrice]:
    if InsurancePrice.objects.count() == 0:
        return EmployerCompanyCoveragePrice.objects.none()

    employees_insurance_prices_pk = [str(employee.user.insurance_prices.latest('created').id)
                                     for employee in employer_company.employees.all()]

    return EmployerCompanyCoveragePrice.objects.filter(user_insurance_price__id__in=employees_insurance_prices_pk)


def get_employer_company_prices(employer_company: EmployerCompany) -> Iterable[EmployerCompanyPrice]:
    return EmployerCompanyPrice.objects.filter(employer_company_id=employer_company.id)


def is_company_price_up_to_date(company_price: EmployerCompanyPrice) -> bool:
    for employer_company_coverage_price in company_price.coverage_prices.all():

        user = employer_company_coverage_price.user_insurance_price.user
        latest_user_insurance_price = get_latest_user_insurance_price(user)

        if employer_company_coverage_price.user_insurance_price != latest_user_insurance_price:
            return False

    return True


def get_regular_partner_discount(employer_company: EmployerCompany) -> float:
    if employer_company.employees.count() >= employer_company.insurance_company.company_employees_num:
        return employer_company.insurance_company.company_sale
    return 0


def get_first_employer_company_price(employer_company: EmployerCompany) -> EmployerCompanyPrice:
    total_price = 0

    for employee in employer_company.employees.all():

        coverage_price = get_latest_user_insurance_price(employee.user)
        total_price += coverage_price.price

    regular_partner_discount = get_regular_partner_discount(employer_company)
    total_price *= 1 - regular_partner_discount

    return EmployerCompanyPrice.objects.create(employer_company=employer_company, price=total_price)


def get_or_create_latest_employer_company_price(employer_company: EmployerCompany) -> EmployerCompanyPrice:
    if EmployerCompanyPrice.objects.count() == 0:
        return get_first_employer_company_price(employer_company)

    latest_company_price: EmployerCompanyPrice = EmployerCompanyPrice.objects.latest('created')

    total_price: int = 0

    for employer_company_coverage_price in latest_company_price.coverage_prices.all():

        user: User = employer_company_coverage_price.user_insurance_price.user
        latest_user_insurance_price: InsurancePrice = get_latest_user_insurance_price(user)

        total_price += latest_user_insurance_price.employer_company_coverage_price.price

    regular_partner_discount = get_regular_partner_discount(employer_company)
    total_price *= 1 - regular_partner_discount

    if total_price == latest_company_price.price:
        return latest_company_price

    return EmployerCompanyPrice.objects.create(employer_company=employer_company, price=total_price)



