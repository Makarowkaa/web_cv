from django.shortcuts import render, get_object_or_404
from django.views import View
from .forms import CompanySelectionForm
from .models import Company
import logging

logger = logging.getLogger(__name__)


class CompanyView(View):
    template_name = 'companies/companies.html'
    form_class = CompanySelectionForm

    def get(self, request, *args, **kwargs):
        logger.debug('Rendering CompannyView')
        form = self.form_class()
        companies = Company.objects.all()

        context = {
            'form': form,
            'companies': companies,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        logger.debug('Processing CompannyView POST')
        form = self.form_class(request.POST)
        companies = []

        if form.is_valid():
            selected_companies = form.cleaned_data['companies']
            for company in selected_companies:
                companies.append(company)

        context = {
            'form': form,
            'companies': companies,
        }

        return render(request, self.template_name, context)


class CompanyListView(View):
    """
    A view for listing all companies

    Attributes:
        template_name (str): The name of the template

    Methods:
        get: Renders the template
    """
    template_name = 'companies/all_companies.html'

    def get(self, request, *args, **kwargs):
        """
        Renders the template

        Args:
            request (HttpRequest): The request object

        Returns:
            HttpResponse: The response object
        """
        companies = Company.objects.all()

        context = {
            'companies': companies
        }

        return render(request, self.template_name, context)


class CompanyDetailsView(View):
    """
    A view for displaying the details of a company

    Attributes:
        template_name (str): The name of the template

    Methods:
        get: Renders the template
    """
    template_name = 'companies/company_detail.html'

    def get(self, request, *args, **kwargs):
        """
        Renders the template

        Args:
            request (HttpRequest): The request object

        Returns:
            HttpResponse: The response object
        """
        company = get_object_or_404(Company, pk=kwargs['pk'])

        context = {
            'company': company
        }

        return render(request, self.template_name, context)
