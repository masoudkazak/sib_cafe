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
    DAYS = [
        ("0", "Everyday"),
        ("1", "Monday"),
        ("2", "Tuesday"),
        ("3", "Wednesday"),
        ("4", "Saturday"),
        ("5", "Sunday")
    ]
    food = models.OneToOneField(Food, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(blank=True, null=True, verbose_name=_("amount"))
    days = models.CharField(choices=DAYS, max_length=1, default="0", verbose_name=_("days"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["food", "amount"]
        verbose_name_plural = _("fooditems")
        verbose_name = _("fooditem")
    
    def __str__(self):
        return f"{self.food.title} - {self.amount}"


class OrderItem(models.Model):
    STATUS = [
        ("0", "Order"),
        ("1", "Cancel"),
        ("2", "Accept"),
        ("3", "Paid"),
        ("4", "Debt")
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1, verbose_name=_("amount"))
    status = models.CharField(choices=STATUS, max_length=1, default=0, verbose_name=_("status"))
    real_price = models.PositiveIntegerField(default=0, verbose_name=_("real_price"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["updated", "status"]
        verbose_name_plural = _("orderitems")
        verbose_name = _("orderitem")
    
    def total_price(self):
        price = int(self.amount * self.food.price)
        return price
    
    def real_price(self):
        if not self.real_price and (self.status == "3" or self.status == "4"):
            self.real_price += self.total_price()
    
    def __str__(self):
        return self.user.username


class Review(models.Model):
    POINTS = [
        ("1", "One Point"),
        ("2", "Two Points"),
        ("3", "Three Points"),
        ("4", "Four Points"),
        ("5", "Five Points"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    value = models.CharField(choices=POINTS, max_length=1, default="5", verbose_name=_("value"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["food"]
        verbose_name_plural = _("reviews")
        verbose_name = _("review")
    
    def __str__(self):
        return self.food.title
