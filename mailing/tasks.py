from django.conf import settings
from django.core.mail import EmailMessage

from celery import shared_task

from companies.models import Company


@shared_task(bind=True)
def send_email_task(self, subject, cover_letter, cv, selected_company_ids, user_email):
    """
    A task for sending emails to the selected companies

    Args:
        subject (str): The subject of the email
        cover_letter (str): The cover letter
        cv (File): The CV
        selected_company_ids (list): A list of selected company ids
    """

    companies = Company.objects.filter(id__in=selected_company_ids)

    email = EmailMessage(
        subject=subject,
        body=cover_letter,
        from_email=settings.EMAIL_HOST_USER,
        bcc=[company.email for company in companies],
        reply_to=[user_email],
    )

    email.attach(cv.name, cv.read(), cv.content_type)

    email.send()
