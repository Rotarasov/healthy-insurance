from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from insurance_companies.models import InsuranceCompany
from users.models import EmployedUser, EmployerCompanyRepresentative, EmployedUserMore, \
    EmployerCompanyRepresentativeMore
from .models import EmployerCompany


User = get_user_model()


class EmployeeAPITestCase(APITestCase):
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

    def test_employee_list(self):
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
        response = self.client.get(self.employee_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'emp1@example.com')
        self.assertEqual(response.data['first_name'], 'Test')
        self.assertEqual(response.data['last_name'], 'User1')

    def test_employee_update(self):
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
        response = self.client.delete(self.employee_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class EmployerCompanyRepresentativeAPITestCase(APITestCase):
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

    def test_representative_list(self):
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
        response = self.client.get(self.representative_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'ecr1@example.com')
        self.assertEqual(response.data['first_name'], 'Test')
        self.assertEqual(response.data['last_name'], 'User1')

    def test_representative_update(self):
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
        response = self.client.delete(self.representative_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

