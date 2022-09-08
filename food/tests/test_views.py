import pytest
from rest_framework import status


@pytest.mark.django_db
def test_menu(api_client):
    response = api_client.get("/api/menu/")
    assert response.status_code == status.HTTP_200_OK
