from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from insurance_companies.models import InsuranceCompany
from users.models import EmployedUser
from .models import EmployerCompany


User = get_user_model()


class EmployerCompanyAPITestCase(APITestCase):
    def setUp(self) -> None:
        ins_comp = InsuranceCompany.objects.create(name='ins_c1', individual_price=700, family_price=20000)
        emp_comp = EmployerCompany.objects.create(name='emp_comp1', industry='ind1', insurance_company=ins_comp)
        emp_user = EmployedUser.objects.create_user('emp1@example.com', 'empp1', 'Test', 'User1', '1980-01-01',
                                                    employer_company=emp_comp)
        self.employee_url = reverse('employer_companies:employees', kwargs={'pk': emp_comp.id})

    def test_employee_list(self):
        response = self.client.get(self.employee_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_employee_create(self):
        emp_comp = EmployerCompany.objects.first()
        data = {'email': 'emp2@example.com', 'password': 'empp2', 'confirm_password': 'empp2',
                'first_name': 'Test', 'last_name': 'User2', 'date_of_birth': '1980-01-01',
                'employer_company': emp_comp.id}
        response = self.client.post(self.employee_url, data=data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], 'emp2@example.com')
        self.assertEqual(response.data['first_name'], 'Test')
        self.assertEqual(response.data['last_name'], 'User2')

