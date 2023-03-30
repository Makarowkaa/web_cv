from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings

import os


class MailingForm(forms.Form):
    subject = forms.CharField(max_length=100)
    cover_letter = forms.CharField(widget=forms.Textarea)
    cv = forms.FileField(label='CV (PDF, DOC, DOCX, 1 MB max)')

    def clean_cv(self):
        cv = self.cleaned_data['cv']
        if cv.size > settings.MAX_UPLOAD_SIZE:
            raise ValidationError(_('File too large. Max size allowed is 1 MB.'))
        ext = os.path.splitext(cv.name)[1]
        valid_extensions = ['.pdf', '.doc', '.docx']
        if not ext.lower() in valid_extensions:
            raise ValidationError(_('Unsupported file extension.'))
        return cv
