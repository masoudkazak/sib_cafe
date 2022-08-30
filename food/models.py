from xmlrpc.client import TRANSPORT_ERROR
from django.db import models
from slugify import slugify
from django.core.validators import MaxValueValidator
from django.utils.translation import gettext_lazy as _
from taggit.managers import TaggableManager
from django.contrib.auth.models import User


class Food(models.Model):
    title = models.CharField(max_length=25, verbose_name=_("title"), unique=True)
    image = models.ImageField(upload_to="%Y/%m/%d/", verbose_name=_("image"), blank=True, null=True)
    price = models.PositiveIntegerField(verbose_name=_("price"))
    discount = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)], verbose_name=_("discount"))
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
    
    def final_price(self):
        price = int((1 - 0.01*self.discount) * self.price)
        return price

    def __str__(self):
        return self.title  


class FoodItem(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(verbose_name=_("amount"))
    days = TaggableManager()
    is_limit = models.BooleanField(default=True, verbose_name=_("is_limit"))
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
    amount = models.PositiveIntegerField(default=1)
    status = models.CharField(choices=STATUS, max_length=1, default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["user", "food"]
        verbose_name_plural = _("orderitems")
        verbose_name = _("orderitem")
    
    def get_price(self):
        if self.amount:
            price = int(self.amount * self.food.final_price())
            return price
        return self.food.final_price()
    
    def __str__(self):
        return self.user.username


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    orders = models.ManyToManyField(OrderItem)
    debt =models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated"]
        verbose_name_plural =  _("oredrs")
        verbose_name = _("ordeer")
    
    def get_total_price(self):
        if self.orders.all():
            price = 0
            for item in self.orders.all():
                price += item.get_price()
            return price
        return 0
    
    def __str__(self):
        return f"{self.user.username} - {self.updated}"
