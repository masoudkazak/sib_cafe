import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db


def test_user_register_creation(api_client):
    user_create = {
        "first_name":"mammad",
        "last_name":"mammadi",
        "username":"mammad",
        "email":"mammad@gmail.com",
        "password":"mammad123",
        "password2":"mammad123",
    }
    response = api_client.post(reverse("account:register"), user_create)
    assert response.status_code == status.HTTP_201_CREATED


def test_user_register_not_equal_password(api_client):
    user_create = {
        "first_name":"mammad",
        "last_name":"mammadi",
        "username":"mammad",
        "email":"mammad@gmail.com",
        "password":"mammad123",
        "password2":"123mammad",
    }
    response = api_client.post(reverse("account:register"), user_create)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_debts_request_not_superuser(api_client, user_create_fixture):
    api_client.force_authenticate(user=user_create_fixture)
    response = api_client.get(reverse("account:debts"))
    assert response.status_code == status.HTTP_302_FOUND
