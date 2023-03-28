from django.test import TestCase
from companies.forms import CompanySelectionForm
from companies.models import Company


class CompanySelectionFormTestCase(TestCase):
    def setUp(self):
        self.company1 = Company.objects.create(company_name='Company 1')
        self.company2 = Company.objects.create(company_name='Company 2')

    def test_valid_form(self):
        form_data = {'companies': [self.company1.pk]}
        form = CompanySelectionForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {'companies': []}
        form = CompanySelectionForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_queryset(self):
        form = CompanySelectionForm()
        self.assertQuerysetEqual(form.fields['companies'].queryset.order_by('id'), Company.objects.all().order_by('id'),
                                 transform=lambda x: x)
