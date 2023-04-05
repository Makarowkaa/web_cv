from django.test import TestCase

from companies.models import Company


class CompanyTestCase(TestCase):
    def test_create_and_get_by_id(self):
        company = Company.create('Test Company', 'Test Country', 'test@test.com', 'http://www.test.com')
        self.assertIsNotNone(company.id)
        self.assertEqual(company.company_name, 'Test Company')
        self.assertEqual(company.country, 'Test Country')
        self.assertEqual(company.email, 'test@test.com')
        self.assertEqual(company.website, 'http://www.test.com')
        retrieved_company = Company.get_by_id(company.id)
        self.assertEqual(retrieved_company, company)

    def setUp(self):
        self.company = Company.create('Test Company', 'Test Country', 'test@test.com', 'http://www.test.com')

    def test_get_all(self):
        companies = Company.get_all()
        self.assertIn(self.company, companies)

    def test_get_by_name(self):
        companies = Company.get_by_name('Test')
        self.assertIn(self.company, companies)

    def test_get_by_country(self):
        companies = Company.get_by_country('Test')
        self.assertIn(self.company, companies)

    def test_get_by_email(self):
        companies = Company.get_by_email('test')
        self.assertIn(self.company, companies)

    def test_delete_by_id(self):
        self.assertTrue(Company.delete_by_id(self.company.id))
        self.assertIsNone(Company.get_by_id(self.company.id))

    def test_update(self):
        self.company.update('New Company Name', 'New Country', 'new@test.com', 'http://www.new.com')
        updated_company = Company.get_by_id(self.company.id)
        self.assertEqual(updated_company.company_name, 'New Company Name')
        self.assertEqual(updated_company.country, 'New Country')
        self.assertEqual(updated_company.email, 'new@test.com')
        self.assertEqual(updated_company.website, 'http://www.new.com')
