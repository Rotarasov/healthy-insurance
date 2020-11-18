from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import (
    UnemployedUser,
    EmployedUser,
    EmployerCompanyRepresentative
)
from employer_companies.models import EmployerCompany
from insurance_companies.models import InsuranceCompany


User = get_user_model()


class UserManagerTestCase(TestCase):
    def setUp(self) -> None:
        EmployerCompanyRepresentative.objects.create_user('ecr1@example.com', 'ecrp1', 'Test', 'User1', '1980-01-01')
        UnemployedUser.objects.create_user('un1@example.com', 'unp1', 'Test', 'User1', '1980-01-01')
        ins_comp = InsuranceCompany.objects.create(name='ins_c1', individual_price=700, family_price=20000)
        emp_comp = EmployerCompany.objects.create(name='emp_comp1', industry='ind1', insurance_company=ins_comp)
        EmployedUser.objects.create_user('emp1@example.com', 'empp1', 'Test', 'User1', '1980-01-01',
                                         employer_company=emp_comp)

    def test_user_read(self):
        unemployed_user = UnemployedUser.objects.first()
        self.assertEqual(unemployed_user.role, User.Roles.UNEMPLOYED)
        self.assertEqual(UnemployedUser.objects.count(), 1)
        self.assertEqual(unemployed_user.email, 'un1@example.com')
        self.assertNotEqual(unemployed_user.password, 'unp1')

        employed_user = EmployedUser.objects.first()
        self.assertEqual(employed_user.role, User.Roles.EMPLOYED)
        self.assertEqual(EmployedUser.objects.count(), 1)
        self.assertEqual(employed_user.email, 'emp1@example.com')
        self.assertNotEqual(employed_user.password, 'empp1')

        employer_company_representative = EmployerCompanyRepresentative.objects.first()
        self.assertEqual(employer_company_representative.role, User.Roles.EMPLOYER_COMPANY_REPRESENTATIVE)
        self.assertEqual(EmployerCompanyRepresentative.objects.count(), 1)
        self.assertEqual(employer_company_representative.email, 'ecr1@example.com')
        self.assertNotEqual(employer_company_representative.password, 'ecrp1')
        self.assertEqual(User.objects.count(), 3)

    def test_user_delete(self):
        EmployerCompany.objects.first().delete()
        self.assertEqual(EmployerCompanyRepresentative.objects.count(), 1)

    def test_employer_company_for_user(self):
        ins_comp = InsuranceCompany.objects.create(name='ins_c2', individual_price=700, family_price=20000)
        emp_company = EmployerCompany.objects.create(name='emp_c2', industry='ind2', insurance_company=ins_comp)
        emp_user = EmployedUser.objects.first()
        emp_company.employees.add(emp_user)
        self.assertEqual(emp_user.employer_company.name, 'emp_c2')
        self.assertEqual(emp_user.employer_company.industry, 'ind2')

    def test_insurance_company_for_user(self):
        ins_company = InsuranceCompany.objects.create(name='ins_c2', individual_price=700, family_price=20000)
        user = User.objects.first()
        ins_company.clients.add(user)
        self.assertEqual(user.insurance_company.name, 'ins_c2')
        self.assertEqual(user.insurance_company.individual_price, 700)


class UserAPITestCase(APITestCase):
    user_create_url = reverse('users:create')

    def setUp(self) -> None:
        user = EmployerCompanyRepresentative.objects.create_user('ecr1@example.com', 'ecrp1', 'Test', 'User1',
                                                                 '1980-01-01')
        self.user_detail_url = reverse('users:detail', kwargs={'pk': user.id})

    def test_user_creation(self):
        data = {'email': 'ecr2@example.com', 'password': 'ecrp2', 'confirm_password': 'ecrp2',
                'first_name': 'Test', 'last_name': 'User2', 'date_of_birth': '1980-01-01',
                'role': User.Roles.EMPLOYER_COMPANY_REPRESENTATIVE}
        response = self.client.post(self.user_create_url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], 'ecr2@example.com')
        self.assertEqual(response.data['first_name'], 'Test')
        self.assertEqual(response.data['last_name'], 'User2')
        self.assertEqual(response.data['date_of_birth'], '1980-01-01')
        self.assertIsNone(response.data.get('confirm_password', None))
        self.assertIsNone(response.data.get('password', None))
        self.assertEqual(EmployerCompanyRepresentative.objects.count(), 2)

    def test_user_read(self):
        response = self.client.get(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'ecr1@example.com')
        self.assertEqual(response.data['first_name'], 'Test')
        self.assertEqual(response.data['last_name'], 'User1')
        self.assertEqual(response.data['date_of_birth'], '1980-01-01')

    def test_user_delete(self):
        response = self.client.delete(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
