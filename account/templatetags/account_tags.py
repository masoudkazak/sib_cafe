import re
from django import template
from food.models import OrderItem
from django.db.models import Sum


register = template.Library()

@register.filter
def get_user_debt(value, id):
    total_debt = OrderItem.objects.filter(status=4, user=id).aggregate(Sum("real_price"))
    total_debt = str(total_debt)
    return total_debt[20:-1]
