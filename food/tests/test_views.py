import pytest
from rest_framework import status
from django.urls import reverse
import random


pytestmark = pytest.mark.django_db


def test_menu(api_client):
    response = api_client.get(reverse("food:menu"))
    assert response.status_code == status.HTTP_200_OK


def test_menuitem_HTTP_200(api_client, fooditem_create):
    response = api_client.get(reverse("food:menuitem", kwargs={"slug":"chelo"}))
    assert response.status_code == status.HTTP_200_OK


def test_menuitem_HTTP_404(api_client):
    response = api_client.get(reverse("food:menuitem", kwargs={"slug":"kabab"}))
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_order_HTTP_201(api_client, food_create_fixture, user_create_fixture):
    api_client.force_authenticate(user=user_create_fixture)
    order_create = {
        "food":food_create_fixture.id,
        "status":0,
        "user":user_create_fixture.id,
    }

    response = api_client.post(reverse("food:order-create"), order_create)
    assert response.status_code == status.HTTP_201_CREATED


def test_create_order_validate_status_HTTP_400(api_client, food_create_fixture, user_create_fixture):
    api_client.force_authenticate(user=user_create_fixture)
    order_create = {
        "food":food_create_fixture.id,
        "status":random.randint(1,4),
        "user":user_create_fixture.id,
    }

    response = api_client.post(reverse("food:order-create"), order_create)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_order_validate_day_HTTP_400(api_client, fooditem_create_bad_days, user_create_fixture):
    api_client.force_authenticate(user=user_create_fixture)
    order_create = {
        "food":fooditem_create_bad_days.food.id,
        "status":0,
        "user":user_create_fixture.id,
    }
    print(fooditem_create_bad_days.days)
    response = api_client.post(reverse("food:order-create"), order_create)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

