from django.shortcuts import render
from django.views import View

from .forms import MailingForm
from .tasks import send_email_task


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
            A rendered template with the email sending form

        """
        form = self.form_class(request.POST, request.FILES)
        selected_company_ids = request.session.get('selected_company_ids', [])

        if form.is_valid():
            subject = form.cleaned_data['subject']
            cover_letter = form.cleaned_data['cover_letter']
            cv = request.FILES.get('cv')
            user_email = form.cleaned_data['user_email']

            send_email_task.delay(subject, cover_letter, cv, selected_company_ids, user_email)

            del request.session['selected_company_ids']

        context = {
            'form': form,
            'selected_company_ids': selected_company_ids,
        }

        return render(request, self.template_name, context)
