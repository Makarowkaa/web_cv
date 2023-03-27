from django import forms
from .models import Company


class CompanySelectionForm(forms.Form):
    """
    A form for selecting companies

    Attributes:
        companies (ModelMultipleChoiceField): A multiple choice field for selecting companies
    """
    companies = forms.ModelMultipleChoiceField(queryset=Company.objects.all(), widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['companies'].queryset = Company.objects.all()
