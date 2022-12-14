from django.contrib import admin
from .models import *


class FoodItemInline(admin.TabularInline):
    model = FoodItem


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ["title", "price", "updated"]
    list_editable = ['price']
    search_fields = ["title", "description"]
    prepopulated_fields = {"slug": ("title",)}
    inlines = [FoodItemInline]


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ["food", "amount", "days"]
    list_filter = ["days", "food__is_limit"]
    search_fields = ["food__title"]
    list_editable = ["amount", "days"]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["user", "food", "status", "updated"]
    ordering = ["-updated"]
    list_filter = ["created", "status"]
    search_fields = ['user__username']
    actions = ["make_accept", "make_paid"]
    list_editable = ["status"]

    @admin.action(description="Accept")
    def make_accept(self, request, queryset):
        queryset.update(status="2")

    @admin.action(description="Paid")
    def make_paid(self, request, queryset):
        queryset.update(status="3")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["food", "value", "user"]
    search_fields = ["food__title"]
