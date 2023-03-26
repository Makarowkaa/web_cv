from django.shortcuts import render, get_object_or_404
from django.views import View
from .forms import CompanySelectionForm
from .models import Company


class CompanyView(View):
    template_name = 'companies/companies.html'
    form_class = CompanySelectionForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        companies = []

        context = {
            'form': form,
            'companies': companies
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        companies = []

        if form.is_valid():
            companies = form.filter_companies()

        context = {
            'form': form,
            'companies': companies
        }

        return render(request, self.template_name, context)


class CompanyListView(View):
    template_name = 'companies/all_companies.html'

    def get(self, request, *args, **kwargs):
        companies = Company.objects.all()

        context = {
            'companies': companies
        }

        return render(request, self.template_name, context)


class CompanyDetailsView(View):
    template_name = 'companies/company_detail.html'

    def get(self, request, *args, **kwargs):
        company = get_object_or_404(Company, pk=kwargs['pk'])

        context = {
            'company': company
        }

        return render(request, self.template_name, context)
