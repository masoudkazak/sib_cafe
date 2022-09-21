import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_create_fixture():
    user = user = User.objects.create_user(
        username="someone1",
        password="something"
        )
    return user