from django.conf import settings
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from companies.models import Company
from mailing.tasks import send_email_task


class SendEmailTaskTestCase(TestCase):
    def setUp(self):
        self.company1 = Company.objects.create(company_name='Company 1', email='company1@example.com')
        self.company2 = Company.objects.create(company_name='Company 2', email='company2@example.com')
        self.subject = 'Test email subject'
        self.cover_letter = 'Test email body'
        self.cv = SimpleUploadedFile('test_cv.pdf', b'Test CV content', content_type='application/pdf')
        self.selected_company_ids = [self.company1.id, self.company2.id]

    def test_send_email_task(self):
        send_email_task(self.subject, self.cover_letter, self.cv, self.selected_company_ids)

        # Assert that emails were sent to both companies
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(set(mail.outbox[0].bcc), {self.company1.email, self.company2.email})

        # Assert that the email subject and body are correct
        self.assertEqual(mail.outbox[0].subject, self.subject)
        self.assertEqual(mail.outbox[0].body, self.cover_letter)

        # Assert that the CV attachment is present and has the correct name and content
        self.assertEqual(len(mail.outbox[0].attachments), 1)
        self.assertEqual(mail.outbox[0].attachments[0][0], 'test_cv.pdf')
        self.assertEqual(mail.outbox[0].attachments[0][1], b'Test CV content')

        # Assert that the email was sent from the correct address and has the correct reply-to address
        self.assertEqual(mail.outbox[0].from_email, settings.EMAIL_HOST_USER)
        self.assertEqual(mail.outbox[0].reply_to, [settings.EMAIL_HOST_USER])
