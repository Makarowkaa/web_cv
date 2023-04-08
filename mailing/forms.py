import os

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class MailingForm(forms.Form):
    """
    A form for sending emails

    Attributes:
        subject (CharField): A field for the subject of the email
        cover_letter (CharField): A field for the cover letter
        cv (FileField): A field for the CV

    Methods:
        clean_cv: A method for validating the CV
    """
    subject = forms.CharField(max_length=100)
    cover_letter = forms.CharField(widget=forms.Textarea)
    cv = forms.FileField(label='CV (PDF, DOC, DOCX, 1 MB max)')
    user_email = forms.EmailField(label='Your email')

    def clean_cv(self):
        """
        A method for validating the CV

        Returns:
            cv: The cleaned CV
        """
        cv = self.cleaned_data['cv']
        if cv.size > settings.MAX_UPLOAD_SIZE:
            raise ValidationError(_('File too large. Max size allowed is 1 MB.'))
        ext = os.path.splitext(cv.name)[1]
        valid_extensions = ['.pdf', '.doc', '.docx']
        if not ext.lower() in valid_extensions:
            raise ValidationError(_('Unsupported file extension.'))
        return cv
