from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from employer_companies.models import EmployerCompany
from users.models import EmployedUser, EmployedUserMore
from .models import InsuranceCompany


class InsuranceCompanyAPITestCase(APITestCase):
    obtain_token_url = reverse('users:token-obtain-pair')

    def setUp(self) -> None:
        self.ins_comp = InsuranceCompany.objects.create(name='ins_c1', individual_price=700, family_price=20000)
        self.emp_company = EmployerCompany.objects.create(name='emp_c1', industry='ind1',
                                                          insurance_company=self.ins_comp)
        self.employed1 = EmployedUser.objects.create_user('emp1@example.com', 'empp1', 'Test', 'User1', '1980-01-01')
        EmployedUserMore.objects.create(user=self.employed1, employer_company=self.emp_company, job='job1')

        self.employed2 = EmployedUser.objects.create_user('emp2@example.com', 'empp2', 'Test', 'User2', '1980-01-01')
        EmployedUserMore.objects.create(user=self.employed2, employer_company=self.emp_company, job='job1')

        self.companies_url = reverse('insurance_companies:companies', kwargs={'pk': self.ins_comp.id})
        self.clients_url = reverse('insurance_companies:clients', kwargs={'pk': self.ins_comp.id})

    def set_credentials(self):
        response = self.client.post(self.obtain_token_url, data={'email': 'emp1@example.com', 'password': 'empp1'})
        access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def test_company_list(self):
        self.set_credentials()
        response = self.client.get(self.companies_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_unemployed_clients_list(self):
        self.set_credentials()
        response = self.client.get(self.clients_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

