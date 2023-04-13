from django.conf import settings
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from companies.models import Company
from mailing.forms import MailingForm
from mailing.tasks import send_email_task


class MailingViewTestCase(TestCase):
    def setUp(self):

        # Create two company objects to use in the tests
        self.company1 = Company.objects.create(company_name='Company 1', email='company1@example.com')
        self.company2 = Company.objects.create(company_name='Company 2', email='company2@example.com')

        # Set up values to be used in the tests
        self.subject = 'Test email subject'
        self.cover_letter = 'Test email body'
        self.cv = SimpleUploadedFile('test_cv.pdf', b'Test CV content', content_type='application/pdf')
        self.selected_company_ids = [self.company1.id, self.company2.id]
        self.user_email = 'user@example.com'

        # Set up a client to simulate a user's interaction with the app
        self.client = Client()
        self.client.session['selected_company_ids'] = self.selected_company_ids
        self.client.session['user_email'] = self.user_email
        self.client.session.save()

        # Set the URL for the view being tested
        self.url = reverse('send_email')

    def test_get(self):
        # Test that the GET request to the URL returns a 200 response
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # Test that the response uses the expected template and contains a MailingForm object in its context
        self.assertTemplateUsed(response, 'mailing/send_email.html')
        self.assertIsInstance(response.context['form'], MailingForm)

    def test_post(self):

        # Simulate a POST request with the form data and CV attachment
        response = self.client.post(self.url, {
            'subject': self.subject,
            'cover_letter': self.cover_letter,
            'selected_company_ids': self.selected_company_ids,
            'user_email': self.user_email,
        }, file={'cv': self.cv})

        # Test that the view returns a 200 response
        self.assertEqual(response.status_code, 200)

        # Simulate the task being run
        send_email_task(self.subject, self.cover_letter, self.cv, self.selected_company_ids, self.user_email)

        # Test that one email has been sent and that it has the expected properties
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(set(mail.outbox[0].bcc), {self.company1.email, self.company2.email})
        self.assertEqual(mail.outbox[0].subject, self.subject)
        self.assertEqual(mail.outbox[0].body, self.cover_letter)
        self.assertEqual(len(mail.outbox[0].attachments), 1)
        attachment = mail.outbox[0].attachments[0]

        # Check attachment name and content
        self.assertEqual(attachment[0], 'test_cv.pdf')
        self.assertEqual(attachment[1], b'Test CV content')

        # Check the sender and reply-to addresses
        self.assertEqual(mail.outbox[0].from_email, settings.EMAIL_HOST_USER)
        self.assertEqual(mail.outbox[0].reply_to, [self.user_email])
