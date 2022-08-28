from tabnanny import verbose
from venv import create
from django.db import models
import slugify
from django.core.validators import MaxValueValidator
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=10, verbose_name=_("name"))

    class Meta:
        ordering = ["name"]
        verbose_name_plural = _("categories")
        verbose_name = _("category")
    
    def __str__(self):
        return self.name


class Food(models.Model):
    title = models.CharField(max_length=25, verbose_name=_("title"))
    category = models.ManyToManyField(Category, verbose_name=_("category"))
    image = models.ImageField(upload_to="%Y/%m/%d/", verbose_name=_("image"))
    price = models.PositiveIntegerField(verbose_name=_("price"))
    discount = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(100)], verbose_name=_("discount"))
    description = models.TextField(blank=True, null=True, verbose_name=_("description"))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    slug = models.SlugField()

    class Meta:
        ordering = ["title", "-price"]
        verbose_name_plural = _("foods")
        verbose_name = _("food")

    def save(self, *args, **kwargs):
        self.slug = slugify.slugify(self.name)
        return super().save(*args, **kwargs)
    
    def final_price(self):
        price = (1 - 0.01*self.discount) * self.price
        return price

    def __str__(self):
        return self.title  



class MenuItem(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = _("menuitems")
        verbose_name = _("menuitem")
    
    def __str__(self):
        return f"{self.food.title} - {self.amount}"
    

class Menu(models.Model):
    name = models.CharField(max_length=100)
    foods = models.ManyToManyField(MenuItem)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        verbose_name_plural = _("menus")
        verbose_name = _("menu")
    
    def __str__(self):
        return self.name
 

class OrderItem(models.Model):
    pass


class Order(models.Model):
    pass


class Archive(models.Model):
    pass


class Review(models.Model):
    pass