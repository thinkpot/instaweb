from django.views.generic import TemplateView
from rest_framework import viewsets
from .models import Leads, ServicesProvided
from .serializers import LeadsSerializer, ServicesProvidedSerializer
from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticated, IsAdminUser
import requests
import os

# Your telegram chat ID and API URL should be configured here
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TELEGRAM_API_KEY = os.getenv('TELEGRAM_API_KEY')
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_API_KEY}/sendMessage"


def send_telegram_message(message):
    data = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
    }
    print("Telegram api url ", TELEGRAM_API_URL)
    response = requests.post(TELEGRAM_API_URL, data=data)
    return response


# Custom permission class to allow POST requests for non-admin users
class IsAdminOrPostOnly(BasePermission):
    def has_permission(self, request, view):
        # Allow everyone to make POST requests (creating new leads)
        if request.method == 'POST':
            return True
        # Only allow GET, PUT, DELETE, etc. for admin users
        return request.user and request.user.is_staff


class HomePage(TemplateView):
    template_name = 'homepage.html'

    def get_context_data(self, **kwargs):
        # Get the default context data (if any)
        context = super().get_context_data(**kwargs)
        # Add the services to the context
        context['services'] = ServicesProvided.objects.all()

        return context


class ContactPage(TemplateView):
    template_name = 'contact.html'

    def get_context_data(self, **kwargs):
        # Get the default context data (if any)
        context = super().get_context_data(**kwargs)
        # Add the services to the context
        context['services'] = ServicesProvided.objects.all()

        return context


class AboutPage(TemplateView):
    template_name = 'about.html'


class LeadsViewSet(viewsets.ModelViewSet):
    queryset = Leads.objects.all()
    serializer_class = LeadsSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            # Only admins can make GET requests
            permission_classes = [IsAdminUser]
        else:
            # Non-admins can make POST requests, but not GET, PUT, DELETE, etc.
            permission_classes = [IsAdminOrPostOnly]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        # Save the lead object
        lead = serializer.save()

        # Send a Telegram message with the lead details
        message = f"New Lead Submitted:\n\n" \
                  f"Name: {lead.full_name}\n" \
                  f"Email: {lead.email}\n" \
                  f"Phone: {lead.phone_number}\n" \
                  f"Service Interested: {lead.service_interest.name}"

        send_telegram_message(message)


class ServicesProvidedViewSet(viewsets.ModelViewSet):
    queryset = ServicesProvided.objects.all()
    serializer_class = ServicesProvidedSerializer