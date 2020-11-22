from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from employer_companies.models import EmployerCompany
from users.models import EmployedUser
from .models import InsuranceCompany


class InsuranceCompanyAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.ins_comp = InsuranceCompany.objects.create(name='ins_c1', individual_price=700, family_price=20000)
        self.emp_company = EmployerCompany.objects.create(name='emp_c1', industry='ind1',
                                                          insurance_company=self.ins_comp)
        self.employed1 = EmployedUser.objects.create_user('emp1@example.com', 'empp1', 'Test', 'User1', '1980-01-01',
                                                          insurance_company=self.ins_comp,
                                                          employer_company=self.emp_company)
        self.employed2 = EmployedUser.objects.create_user('emp2@example.com', 'empp2', 'Test', 'User2', '1980-01-01',
                                                          insurance_company=self.ins_comp,
                                                          employer_company=self.emp_company)

        self.companies_url = reverse('insurance_companies:companies', kwargs={'pk': self.ins_comp.id})
        self.clients_url = reverse('insurance_companies:clients', kwargs={'pk': self.ins_comp.id})

    def test_company_list(self):
        response = self.client.get(self.companies_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_clients_list(self):
        response = self.client.get(self.clients_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

