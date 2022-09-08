from rest_framework.filters import BaseFilterBackend

from .models import Food, Review


class OrderingReview(BaseFilterBackend):
    reviews = Review.objects.values_list("id", flat=True).order_by("-value")
    not_value_food = Food.objects.filter()

    def get_list_ids(self):
        return self.reviews.keys()

    def filter_queryset(self, request, queryset, view):
        return queryset
    
    # def get_schema_fields(self, view):
    #     assert coreapi is not None, 'coreapi must be installed to use `get_schema_fields()`'
    #     assert coreschema is not None, 'coreschema must be installed to use `get_schema_fields()`'
    #     return []

    # def get_schema_operation_parameters(self, view):
    #     return []