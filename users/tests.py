from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import (
    UnemployedUser,
    EmployedUser,
    Measurement,
    InsurancePrice
)
from employer_companies.models import EmployerCompany
from insurance_companies.models import InsuranceCompany


User = get_user_model()


class UserManagerTestCase(TestCase):
    def setUp(self) -> None:
        self.ins_comp = InsuranceCompany.objects.create(name='ins_c1', individual_price=700, family_price=20000)
        self.emp_comp = EmployerCompany.objects.create(name='emp_comp1', industry='ind1',
                                                       insurance_company=self.ins_comp)
        self.unemployed = UnemployedUser.objects.create_user('un1@example.com', 'unp1', 'Test', 'User1', '1980-01-01',
                                                             insurance_company=self.ins_comp)
        self.employed = EmployedUser.objects.create_user('emp1@example.com', 'empp1', 'Test', 'User1', '1980-01-01',
                                                         employer_company=self.emp_comp,
                                                         insurance_company=self.ins_comp)

    def test_user_read(self):
        self.assertEqual(self.unemployed.role, User.Roles.UNEMPLOYED)
        self.assertEqual(UnemployedUser.objects.count(), 1)
        self.assertEqual(self.unemployed.email, 'un1@example.com')
        self.assertNotEqual(self.unemployed.password, 'unp1')

        self.assertEqual(self.employed.role, User.Roles.EMPLOYED)
        self.assertEqual(EmployedUser.objects.count(), 1)
        self.assertEqual(self.employed.email, 'emp1@example.com')
        self.assertNotEqual(self.employed.password, 'empp1')

    def test_user_delete(self):
        self.unemployed.delete()
        self.assertEqual(UnemployedUser.objects.count(), 0)

    def test_employer_company_for_user(self):
        ins_comp = InsuranceCompany.objects.create(name='ins_c2', individual_price=700, family_price=20000)
        emp_company = EmployerCompany.objects.create(name='emp_c2', industry='ind2', insurance_company=ins_comp)
        emp_company.employees.add(self.employed)
        self.assertEqual(self.employed.employer_company.name, 'emp_c2')
        self.assertEqual(self.employed.employer_company.industry, 'ind2')

    def test_insurance_company_for_user(self):
        ins_company = InsuranceCompany.objects.create(name='ins_c2', individual_price=700, family_price=20000)
        ins_company.clients.add(self.unemployed)
        self.assertEqual(self.unemployed.insurance_company.name, 'ins_c2')
        self.assertEqual(self.unemployed.insurance_company.individual_price, 700)


class UserAPITestCase(APITestCase):
    unemployed_create_url = reverse('users:unemployed-create')

    def setUp(self) -> None:
        self.ins_comp = InsuranceCompany.objects.create(name='ins_c1', individual_price=700, family_price=20000)
        self.unemployed = UnemployedUser.objects.create_user('un1@example.com', 'unp1', 'Test', 'User1', '1980-01-01',
                                                             insurance_company=self.ins_comp)
        self.unemployed_detail_url = reverse('users:unemployed-detail', kwargs={'pk': self.unemployed.id})
        self.measurement_list_url = reverse('users:measurement-list', kwargs={'pk': self.unemployed.id})

    def test_unemployed_creation(self):
        data = {'email': 'un2@example.com', 'password': 'unp2', 'confirm_password': 'unp2', 'first_name': 'Test',
                'last_name': 'User2', 'date_of_birth': '1980-01-01', 'insurance_company': self.ins_comp.id}
        response = self.client.post(self.unemployed_create_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], 'un2@example.com')
        self.assertEqual(response.data['first_name'], 'Test')
        self.assertEqual(response.data['last_name'], 'User2')
        self.assertEqual(response.data['date_of_birth'], '1980-01-01')
        self.assertIsNone(response.data.get('confirm_password', None))
        self.assertIsNone(response.data.get('password', None))
        self.assertEqual(UnemployedUser.objects.count(), 2)

    def test_user_read(self):
        response = self.client.get(self.unemployed_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'un1@example.com')
        self.assertEqual(response.data['first_name'], 'Test')
        self.assertEqual(response.data['last_name'], 'User1')
        self.assertEqual(response.data['date_of_birth'], '1980-01-01')

    def test_user_delete(self):
        response = self.client.delete(self.unemployed_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_insurance_price(self):
        data = {'start': '2020-10-01T09:00Z', 'end': '2020-10-02T10:00Z', 'sdnn': 60, 'sdann': 60, 'rmssd': 10}
        response = self.client.post(self.measurement_list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.unemployed.insurance_prices.get(measurement_id=response.data['id']).price,
                         self.unemployed.insurance_company.individual_price)

        data['sdnn'] = 90
        data['sdann'] = 100
        data['rmssd'] = 20
        response = self.client.post(self.measurement_list_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(self.unemployed.insurance_prices.get(measurement_id=response.data['id']).price)
        self.assertLess(self.unemployed.insurance_prices.get(measurement_id=response.data['id']).price,
                        self.unemployed.insurance_company.individual_price)


