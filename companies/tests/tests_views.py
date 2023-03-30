from django.test import TestCase, Client
from django.urls import reverse
from companies.models import Company
from companies.forms import CompanySelectionForm


class CompanyViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('companies')
        self.company1 = Company.objects.create(company_name='Company 1')
        self.company2 = Company.objects.create(company_name='Company 2')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], CompanySelectionForm)
        self.assertQuerysetEqual(response.context['companies'], Company.objects.all(),
                                 transform=lambda x: x, ordered=False)

    def test_post_valid(self):
        data = {'companies': [self.company1.id, self.company2.id]}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertListEqual(self.client.session['selected_companies'],
                             [{'id': self.company1.id, 'name': self.company1.company_name},
                              {'id': self.company2.id, 'name': self.company2.company_name}])

    def test_post_invalid(self):
        data = {'companies': [self.company1.id, 999]}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(self.client.session.get('selected_companies'))


class CompanyListViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('all-companies')
        self.company1 = Company.objects.create(company_name='Company 1')
        self.company2 = Company.objects.create(company_name='Company 2')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['companies'], Company.objects.all(),
                                 transform=lambda x: x, ordered=False)


class CompanyDetailsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.company = Company.objects.create(company_name='Company')
        self.url = reverse('company-details', kwargs={'pk': self.company.id})

    def test_get_valid(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['company'], self.company)

    def test_get_invalid(self):
        url = reverse('company-details', kwargs={'pk': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
