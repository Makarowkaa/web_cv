from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .forms import CompanySelectionForm
from .models import Company


class CompanyView(View):
    """
    A view for displaying and choosing the companies

    Attributes:
        template_name (str): The name of the template
        form_class (Form): The form class

    Methods:
        get: Renders the company selection form
        post: Process the form and redirects to the next page
    """
    template_name = 'companies/companies.html'
    form_class = CompanySelectionForm

    def get(self, request, *args, **kwargs):
        """
        Renders the company selection form

        Returns:
            A rendered template with the company selection form and a list of all companies.
        """
        form = self.form_class()
        companies = Company.objects.all()

        context = {
            'form': form,
            'companies': companies,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        Processes the company selection form and redirects to the appropriate page.

        Returns:
            A redirect to the appropriate page.
        """
        form = self.form_class(request.POST)
        selected_companies = []

        if form.is_valid():
            selected_companies = form.cleaned_data['companies']
            company_dicts = []
            for company in selected_companies:
                company_dicts.append({
                    'id': company.id,
                    'name': company.company_name,
                    'email': company.email,
                })
            request.session['selected_companies'] = company_dicts
            return redirect('send_email')

        context = {
            'form': form,
            'companies': selected_companies,
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

        Returns:
            Rendered templates with list of all the companies
        """
        companies = Company.objects.all()

        context = {
            'companies': companies
        }

        return render(request, self.template_name, context)


class CompanyDetailsView(View):
    """
    A view for displaying one company

    Attributes:
        template_name (str): The name of the template

    Methods:
        get: Renders the template
    """
    template_name = 'companies/company_detail.html'

    def get(self, request, *args, **kwargs):
        """
        Renders the template

        Returns:
            Rendered template with the details of the company
        """
        company = get_object_or_404(Company, pk=kwargs['pk'])

        context = {
            'company': company
        }

        return render(request, self.template_name, context)
