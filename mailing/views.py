from django.shortcuts import render, redirect
from django.views import View
from django.core.mail import EmailMessage
from django.conf import settings

from .forms import MailingForm
from companies.models import Company


class MailingView(View):
    """
    A view for sending emails to the selected companies

    Attributes:
        template_name (str): The name of the template
        form_class (Form): The form class

    Methods:
        get: Renders the email sending form
        post: Process the form and redirects to the next page
    """
    template_name = 'mailing/send_email.html'
    form_class = MailingForm

    def get(self, request, *args, **kwargs):
        """
        Renders the email sending form

        Returns:
            A rendered template with the email sending form
        """
        form = self.form_class()
        selected_company_ids = request.session.get('selected_company_ids', [])

        context = {
            'form': form,
            'selected_company_ids': selected_company_ids,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        Processes the email sending form and redirects to the appropriate page.

        Returns:
            A redirect to the appropriate page.

        """
        form = self.form_class(request.POST, request.FILES)
        selected_company_ids = request.session.get('selected_company_ids', [])

        if form.is_valid():
            subject = form.cleaned_data['subject']
            cover_letter = form.cleaned_data['cover_letter']
            cv = request.FILES.get('cv')

            companies = Company.objects.filter(id__in=selected_company_ids)

            for company in companies:
                email = EmailMessage(
                    subject=subject,
                    body=cover_letter,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[company.email],
                    reply_to=[settings.EMAIL_HOST_USER],
                )

                if cv:
                    email.attach(cv.name, cv.read(), cv.content_type)

                email.send()

            del request.session['selected_company_ids']

            # return redirect('mailing:success')

        context = {
            'form': form,
            'selected_company_ids': selected_company_ids,
        }

        return render(request, self.template_name, context)
