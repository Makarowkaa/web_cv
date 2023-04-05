from django.contrib import admin

from .models import Company


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'company_name', 'country', 'email', 'website')
    list_display_links = ('id', 'company_name')
    search_fields = ('company_name', 'country', 'email', 'website')
    list_per_page = 25


admin.site.register(Company, CompanyAdmin)
