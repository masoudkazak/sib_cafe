from django.db import models
from slugify import slugify
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class Food(models.Model):
    title = models.CharField(max_length=25, verbose_name=_("title"), unique=True)
    image = models.ImageField(upload_to="%Y/%m/%d/", verbose_name=_("image"), blank=True, null=True)
    price = models.PositiveIntegerField(verbose_name=_("price"))
    is_limit = models.BooleanField(default=True, verbose_name=_("is_limit"))
    description = models.TextField(blank=True, null=True, verbose_name=_("description"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField()

    class Meta:
        ordering = ["title", "-price"]
        verbose_name_plural = _("foods")
        verbose_name = _("food")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title  


class FoodItem(models.Model):
    class Days(models.IntegerChoices):
        Monday = 0
        Tuesday = 1
        Wednesday = 2
        Saturday = 5
        Sunday = 6
        Everyday = 7 

    food = models.OneToOneField(Food, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(blank=True, null=True, verbose_name=_("amount"))
    days = models.IntegerField(choices=Days.choices, default=0, verbose_name=_("days"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["food", "amount"]
        verbose_name_plural = _("fooditems")
        verbose_name = _("fooditem")

    def __str__(self):
        return f"{self.food.title} - {self.amount}"


class OrderItem(models.Model):
    class Status(models.IntegerChoices):
        Order = 0
        Cancel = 1
        Accept = 2
        Paid = 3
        Debt = 4

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    status = models.IntegerField(choices=Status.choices, default=0, verbose_name=_("status"))
    real_price = models.PositiveIntegerField(verbose_name=_("real_price"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["updated", "status"]
        verbose_name_plural = _("orderitems")
        verbose_name = _("orderitem")
    
    def __str__(self):
        return self.user.username


class Review(models.Model):
    class Points(models.IntegerChoices):
        zero_point = 0
        one_point = 1
        two_points = 2
        three_points = 3
        four_points = 4
        five_points = 5

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, related_name="reviews", on_delete=models.CASCADE)
    value = models.IntegerField(choices=Points.choices, verbose_name=_("value"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["food"]
        verbose_name_plural = _("reviews")
        verbose_name = _("review")
    
    def __str__(self):
        return self.food.title
