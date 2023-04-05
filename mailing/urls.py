from django.urls import path

from .views import MailingView

urlpatterns = [
    path('send-email', MailingView.as_view(), name='send_email'),
]
