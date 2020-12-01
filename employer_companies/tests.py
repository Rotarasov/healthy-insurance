from datetime import datetime, date

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from insurance_companies.models import InsuranceCompany
from users.models import (
    EmployedUser,
    EmployerCompanyRepresentative,
    EmployedUserMore,
    EmployerCompanyRepresentativeMore,
    Measurement
)
from users.services import create_user_insurance_price, create_company_coverage_price
from .models import EmployerCompany

User = get_user_model()

local_tz = timezone.get_default_timezone()


class EmployeeAPITestCase(APITestCase):
    obtain_token_url = reverse('users:token-obtain-pair')

    def setUp(self) -> None:
        self.ins_comp = InsuranceCompany.objects.create(name='ins_c1', individual_price=700, family_price=20000)
        self.emp_comp = EmployerCompany.objects.create(name='emp_comp1', industry='ind1',
                                                       insurance_company=self.ins_comp)
        self.emp_user = EmployedUser.objects.create_user('emp1@example.com', 'empp1', 'Test', 'User1', '1980-01-01')
        EmployedUserMore.objects.create(user=self.emp_user, employer_company=self.emp_comp, job='job1')
        self.employee_list_url = reverse('employer_companies:employee-list', kwargs={'pk': self.emp_comp.id})
        self.employee_detail_url = reverse('employer_companies:employee-detail',
                                           kwargs={'employer_company_pk': self.emp_comp.id,
                                                   'employee_pk': self.emp_user.id})

    def set_credentials(self):
        response = self.client.post(self.obtain_token_url, data={'email': 'emp1@example.com', 'password': 'empp1'})
        access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def test_employee_list(self):
        self.set_credentials()
        response = self.client.get(self.employee_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_employee_create(self):
        data = {
            'email': 'emp2@example.com',
            'password': 'empp2',
            'confirm_password': 'empp2',
            'first_name': 'Test',
            'last_name': 'User2',
            'date_of_birth': '1980-01-01',
            'employed_user_more':
                {
                    'employer_company': self.emp_comp.id,
                    'job': 'job2'
                }
        }
        response = self.client.post(self.employee_list_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], 'emp2@example.com')
        self.assertEqual(response.data['first_name'], 'Test')
        self.assertEqual(response.data['last_name'], 'User2')

    def test_employee_read(self):
        self.set_credentials()
        response = self.client.get(self.employee_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'emp1@example.com')
        self.assertEqual(response.data['first_name'], 'Test')
        self.assertEqual(response.data['last_name'], 'User1')

    def test_employee_update(self):
        self.set_credentials()
        data = {
            'email': 'emp1@example.com',
            'first_name': 'Test',
            'last_name': 'User11',
            'date_of_birth': '1980-01-01',
            'employed_user_more':
                {
                    'employer_company': self.emp_comp.id,
                    'job': 'job11'
                }
        }
        response = self.client.put(self.employee_detail_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'emp1@example.com')
        self.assertEqual(response.data['first_name'], 'Test')
        self.assertEqual(response.data['last_name'], 'User11')

    def test_employee_delete(self):
        self.set_credentials()
        response = self.client.delete(self.employee_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class EmployerCompanyRepresentativeAPITestCase(APITestCase):
    obtain_token_url = reverse('users:token-obtain-pair')

    def setUp(self) -> None:
        self.ins_comp = InsuranceCompany.objects.create(name='ins_c1', individual_price=700, family_price=20000)
        self.emp_comp = EmployerCompany.objects.create(name='emp_comp1', industry='ind1',
                                                       insurance_company=self.ins_comp)
        self.emp_representative = EmployerCompanyRepresentative.objects.create_user(
            'ecr1@example.com', 'ecrp1', 'Test', 'User1', '1980-01-01',
        )
        EmployerCompanyRepresentativeMore.objects.create(user=self.emp_representative, employer_company=self.emp_comp)
        self.representative_list_url = reverse('employer_companies:representative-list',
                                               kwargs={'pk': self.emp_comp.id})
        self.representative_detail_url = reverse('employer_companies:representative-detail',
                                                 kwargs={'employer_company_pk': self.emp_comp.id,
                                                         'representative_pk': self.emp_representative.id})

    def set_credentials(self):
        response = self.client.post(self.obtain_token_url, data={'email': 'ecr1@example.com', 'password': 'ecrp1'})
        access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def test_representative_list(self):
        self.set_credentials()
        response = self.client.get(self.representative_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_representative_create(self):
        emp_comp2 = EmployerCompany.objects.create(name='emp_comp2', industry='ind2', insurance_company=self.ins_comp)
        data = {
            'email': 'ecr2@example.com',
            'password': 'ecrp2',
            'confirm_password': 'ecrp2',
            'first_name': 'Test',
            'last_name': 'User2',
            'date_of_birth': '1980-01-01',
            'employer_company_representative_more':
                {
                    'employer_company': emp_comp2.id
                }
        }
        response = self.client.post(self.representative_list_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], 'ecr2@example.com')
        self.assertEqual(response.data['first_name'], 'Test')
        self.assertEqual(response.data['last_name'], 'User2')

    def test_representative_read(self):
        self.set_credentials()
        response = self.client.get(self.representative_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'ecr1@example.com')
        self.assertEqual(response.data['first_name'], 'Test')
        self.assertEqual(response.data['last_name'], 'User1')

    def test_representative_update(self):
        self.set_credentials()
        data = {
            'email': 'ecr1@example.com',
            'first_name': 'Test',
            'last_name': 'User11',
            'date_of_birth': '1980-01-01',
            'employer_company_representative_more':
                {
                    'employer_company': self.emp_comp.id,
                }
        }
        response = self.client.put(self.representative_detail_url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'ecr1@example.com')
        self.assertEqual(response.data['first_name'], 'Test')
        self.assertEqual(response.data['last_name'], 'User11')

    def test_representative_delete(self):
        self.set_credentials()
        response = self.client.delete(self.representative_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class EmployerCompanyAPITestCase(APITestCase):
    obtain_token_url = reverse('users:token-obtain-pair')

    def setUp(self) -> None:
        self.ins_comp = InsuranceCompany.objects.create(name='ins_c1', individual_price=700, family_price=20000)
        self.emp_comp = EmployerCompany.objects.create(name='emp_comp1', industry='ind1',
                                                       insurance_company=self.ins_comp)
        self.emp_user = EmployedUser.objects.create_user('emp1@example.com', 'empp1', 'Test', 'User1', date(1980, 1, 1))
        EmployedUserMore.objects.create(user=self.emp_user, employer_company=self.emp_comp, job='job1')
        self.measurement = Measurement.objects.create(start=local_tz.localize(datetime(2020, 10, 1, 9)),
                                                      end=local_tz.localize(datetime(2020, 10, 2, 10)),
                                                      sdnn=90, sdann=100, rmssd=20)
        self.insurance_price = create_user_insurance_price(self.emp_user, self.measurement)
        self.employer_company_coverage_price = create_company_coverage_price(self.insurance_price, self.emp_comp)

        self.employer_company_coverage_price_list = reverse('employer_companies:coverage-price-list',
                                                            kwargs={'pk': self.emp_comp.id})
        self.insurance_price_url = reverse('users:insurance-price', kwargs={'pk': self.emp_user.id})
        self.employer_company_price_create_url = reverse('employer_companies:price-create', kwargs={'pk': self.emp_comp.id})

    def set_credentials(self):
        response = self.client.post(self.obtain_token_url, data={'email': 'emp1@example.com', 'password': 'empp1'})
        access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def test_employer_company_coverage_price_list(self):
        self.set_credentials()
        response = self.client.get(self.employer_company_coverage_price_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['price'], 428)

        response = self.client.get(self.insurance_price_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['price'], 167)

    def test_employer_company_company_price(self):
        self.set_credentials()
        response = self.client.post(self.employer_company_price_create_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['price'], 167)


