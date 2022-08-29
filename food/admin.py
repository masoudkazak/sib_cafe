from django.contrib import admin
from .models import *


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ["title", "price", "discount", "final_price", "updated"]
    list_editable = ['price', "discount"]
    search_fields = ["title", "description"]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ["food", "amount", "total_price", "days_list"]
    list_filter = ["days", "is_limit"]
    search_fields = ["food__title"]
    list_editable = ["amount"]

    actions = ["make_unavailable"]

    def days_list(self, obj):
        return u", ".join(o.name for o in obj.days.all())

    @admin.action(description="Unavailable")
    def make_unavailable(self, request, queryset):
        queryset.update(amount=0)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["user", "food"]
    search_fields = ['user__username']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', "get_items", "" "status"]
    list_editable = ['status']
    list_filter = ["status", "created"]
    search_fields = ["user__username"]

    actions = ["make_accept", "make_paid"]

    def get_items(self, obj):
        result = ""
        for o in obj.orders.all():
            result += f"{o.food.title}({o.amount}), "
        return result
    
    @admin.action(description="Accept")
    def make_accept(self, request, queryset):
        queryset.update(status="2")

    @admin.action(description="Paid")
    def make_paid(self, request, queryset):
        queryset.update(status="3")
