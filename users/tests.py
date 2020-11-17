from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from .models import (
    UnemployedUser,
    EmployedUser,
    InsuranceCompanyRepresentative,
    EmployerCompanyRepresentative
)


User = get_user_model()


class UserManagementAPITestCase(APITestCase):
    def setUp(self) -> None:
        InsuranceCompanyRepresentative.objects.create_user('icr1@example.com', 'icrp1', 'Test', 'User1', '1980-01-01')
        EmployerCompanyRepresentative.objects.create_user('ecr1@example.com', 'ecrp1', 'Test', 'User1', '1980-01-01')
        UnemployedUser.objects.create_user('un1@example.com', 'unp1', 'Test', 'User1', '1980-01-01')
        EmployedUser.objects.create_user('emp1@example.com', 'empp1', 'Test', 'User1', '1980-01-01')

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

        insurance_company_representative = InsuranceCompanyRepresentative.objects.first()
        self.assertEqual(insurance_company_representative.role, User.Roles.INSURANCE_COMPANY_REPRESENTATIVE)
        self.assertEqual(InsuranceCompanyRepresentative.objects.count(), 1)
        self.assertEqual(insurance_company_representative.email, 'icr1@example.com')
        self.assertNotEqual(insurance_company_representative.password, 'icrp1')

        employer_company_representative = EmployerCompanyRepresentative.objects.first()
        self.assertEqual(employer_company_representative.role, User.Roles.EMPLOYER_COMPANY_REPRESENTATIVE)
        self.assertEqual(InsuranceCompanyRepresentative.objects.count(), 1)
        self.assertEqual(employer_company_representative.email, 'ecr1@example.com')
        self.assertNotEqual(employer_company_representative.password, 'ecrp1')

    def test_user_update_password(self):
        unemployed_user = UnemployedUser.objects.first()
        unemployed_user.set_password('unp2')
        unemployed_user.save()
        self.assertTrue(unemployed_user.check_password('unp2'))

    def test_user_delete(self):
        InsuranceCompanyRepresentative.objects.first().delete()
        self.assertEqual(InsuranceCompanyRepresentative.objects.count(), 0)


