from django.conf import settings
from rest_framework.test import APIClient
from model_bakery import baker
import pytest


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticate(api_client):
    def do_authenticate(is_staff=False):
        user = baker.make(settings.AUTH_USER_MODEL)
        user.is_staff = is_staff
        api_client.force_authenticate(user=user)
        return user
    return do_authenticate
