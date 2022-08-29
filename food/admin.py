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
    list_display = ["food", "amount", "total_pirce", "days_list"]
    list_filter = ["days", "is_limit"]
    search_fields = ["food__title"]
    list_editable = ["amount"]

    actions = ["make_unavailable"]

    def days_list(self, obj):
        return u", ".join(o.name for o in obj.days.all())

    @admin.action(description="Unavailable")
    def make_unavailable(self, request, queryset):
        queryset.update(amount=0)