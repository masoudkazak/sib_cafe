import pytest
from rest_framework import status
from django.urls import reverse
import random

from food.models import Food
from django.core.cache import cache


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
        "food":fooditem_create_bad_days.food,
        "status":0,
        "user":user_create_fixture.id,
    }
    response = api_client.post(reverse("food:order-create"), order_create)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_cancel_order_HTTP_200(api_client, orderitem_create_for_cancel):
    order = orderitem_create_for_cancel
    api_client.force_authenticate(user=order.user)
    
    update_order = {
            "food":order.food.pk,
            "status":1
        }
    
    response = api_client.put(reverse(
        "food:order-cancel",
        kwargs={"pk":order.pk,
                "username":order.user.username
        }),
        update_order
        )

    assert response.status_code == status.HTTP_200_OK


def test_cancel_order_validate_status_HTTP_400(api_client, orderitem_create_for_cancel):
    order = orderitem_create_for_cancel
    api_client.force_authenticate(user=order.user)
    
    update_order = {
            "food":order.food.pk,
            "status":2
        }
    
    response = api_client.put(reverse(
        "food:order-cancel",
        kwargs={"pk":order.pk,
                "username":order.user.username
        }),
        update_order
        )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_cancel_order_another_user_submit(api_client, orderitem_create_for_cancel, user_create_fixture):
    order = orderitem_create_for_cancel
    api_client.force_authenticate(user=user_create_fixture)
    
    update_order = {
            "food":order.food.pk,
            "status":1
        }
    
    response = api_client.put(reverse(
        "food:order-cancel",
        kwargs={"pk":order.pk,
                "username":order.user.username
        }),
        update_order
        )

    assert order.status != 1


def test_order_list_HTTP_200(api_client, user_create_fixture):
    api_client.force_authenticate(user=user_create_fixture)
    response = api_client.get(reverse("food:orders"))
    assert response.status_code == status.HTTP_200_OK


def test_review_create_http_201(api_client, user_create_fixture, food_create_fixture):
    api_client.force_authenticate(user=user_create_fixture)
    new_rate = {
        'user':user_create_fixture.pk,
        'food':food_create_fixture.pk,
        'value':5,
    }
    response = api_client.post(reverse("food:add-review"), new_rate)

    assert response.status_code == status.HTTP_201_CREATED 


def test_review_create_validate_value_http_400(api_client, user_create_fixture, food_create_fixture):
    api_client.force_authenticate(user=user_create_fixture)
    new_rate = {
        'user':user_create_fixture.pk,
        'food':food_create_fixture.pk,
        'value':6,
    }
    response = api_client.post(reverse("food:add-review"), new_rate)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_review_create_validate_kind_of_item_http_400(api_client, user_create_fixture, unlimit_food_create_fixture):
    api_client.force_authenticate(user=user_create_fixture)
    new_rate = {
        'user':user_create_fixture.pk,
        'food':unlimit_food_create_fixture.pk,
        'value':0,
    }
    response = api_client.post(reverse("food:add-review"), new_rate)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_reviews_list_HTTP_200(api_client, review_create):
    response = api_client.get(reverse("food:reviews"))
    food = Food.objects.get(title="chelo")
    assert cache.get(food) != None
