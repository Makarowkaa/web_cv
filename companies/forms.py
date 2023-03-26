from django import forms
from .models import Company
import logging

logger = logging.getLogger(__name__)


class CompanySelectionForm(forms.Form):
    """
    A form for selecting companies

    Attributes:
        companies (ModelMultipleChoiceField): A multiple choice field for selecting companies
    """
    companies = forms.ModelMultipleChoiceField(queryset=Company.objects.all(), widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.debug('Initializing form')
        self.fields['companies'].queryset = Company.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        logger.debug('Cleaned data: %s', cleaned_data)
        return cleaned_data
