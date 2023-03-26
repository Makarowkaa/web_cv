from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from .models import Company


class CompanySelectionForm(forms.Form):
    """
    A form for selecting companies

    Attributes:
        company_name (str): The name of the company
        country (str): The country where the company is located
        companies (QuerySet): A queryset containing all companies

    Methods:
        filter_companies: Filters the companies based on the given parameters
    """
    company_name = forms.CharField(label='Company Name', max_length=255)
    country = forms.CharField(label='Country', max_length=255, required=False)
    companies = forms.ModelMultipleChoiceField(queryset=Company.objects.all(), widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['companies'].queryset = Company.objects.none()
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Select Companies',
                'company_name',
                'country',
                'companies'
            ),
            ButtonHolder(
                Submit('submit', 'Submit')
            )
        )

    def filter_companies(self):
        """
        Filters the companies based on the given parameters

        Returns:
            QuerySet: A queryset containing all companies that match the given parameters
        """
        company_name = self.cleaned_data['company_name']
        country = self.cleaned_data['country']
        queryset = Company.objects.all()

        if company_name:
            queryset = queryset.filter(company_name__icontains=company_name)

        if country:
            queryset = queryset.filter(country__icontains=country)

        self.fields['companies'].queryset = queryset

        return queryset
