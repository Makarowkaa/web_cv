from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from mailing.forms import MailingForm


class EmailFormTestCase(TestCase):
    def setUp(self):
        self.form_data = {
            'subject': 'Test Subject',
            'cover_letter': 'Test Cover Letter',
        }
        self.valid_cv_file = SimpleUploadedFile('test_cv.pdf', b'test_cv_content', content_type='application/pdf')
        self.invalid_extension_file = SimpleUploadedFile('test_cv.txt', b'test_cv_content', content_type='text/plain')
        self.invalid_size_file = SimpleUploadedFile('test_cv.pdf', b'test_cv_content' * 1000000,
                                                    content_type='application/pdf')

    def test_valid_form(self):
        form_files = {
            'cv': self.valid_cv_file,
        }
        form = MailingForm(data=self.form_data, files=form_files)
        self.assertTrue(form.is_valid(), form.errors)

    def test_invalid_form(self):
        form_files = {
            'cv': self.valid_cv_file,
        }
        form_data = {
            'subject': '',
            'cover_letter': '',
        }
        form = MailingForm(data=form_data, files=form_files)
        self.assertFalse(form.is_valid())
        self.assertIn('subject', form.errors)
        self.assertIn('cover_letter', form.errors)
        self.assertNotIn('cv', form.errors)

    def test_invalid_extension(self):
        form_files = {
            'cv': self.invalid_extension_file,
        }
        form = MailingForm(data=self.form_data, files=form_files)
        self.assertFalse(form.is_valid())
        self.assertNotIn('subject', form.errors)
        self.assertNotIn('cover_letter', form.errors)
        self.assertIn('cv', form.errors)
        self.assertEqual(form.errors['cv'], ['Unsupported file extension.'])

    def test_invalid_file_size(self):
        form_files = {
            'cv': self.invalid_size_file,
        }
        form = MailingForm(data=self.form_data, files=form_files)
        self.assertFalse(form.is_valid())
        self.assertNotIn('subject', form.errors)
        self.assertNotIn('cover_letter', form.errors)
        self.assertIn('cv', form.errors)
        self.assertEqual(form.errors['cv'], ['File too large. Max size allowed is 1 MB.'])
