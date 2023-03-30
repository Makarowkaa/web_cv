from django.shortcuts import render, redirect
from django.views import View
from django.core.mail import EmailMessage
from django.conf import settings

from .forms import MailingForm


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
        selected_companies = request.session.get('selected_companies', [])

        context = {
            'form': form,
            'selected_companies': selected_companies,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        Processes the email sending form and redirects to the appropriate page.

        Returns:
            A redirect to the appropriate page.

        """
        form = self.form_class(request.POST, request.FILES)
        selected_companies = request.session.get('selected_companies', [])

        if form.is_valid():
            subject = form.cleaned_data['subject']
            cover_letter = form.cleaned_data['cover_letter']
            cv = request.FILES.get('cv')

            recipients = [company['email'] for company in selected_companies]

            email = EmailMessage(
                subject=subject,
                body=cover_letter,
                from_email=settings.EMAIL_HOST_USER,
                to=recipients,
                reply_to=[settings.EMAIL_HOST_USER],
            )

            if cv:
                email.attach(cv.name, cv.read(), cv.content_type)

            email.send()

            del request.session['selected_companies']

            # return redirect('mailing:success')

        context = {
            'form': form,
            'selected_companies': selected_companies,
        }

        return render(request, self.template_name, context)
