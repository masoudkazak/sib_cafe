# Generated by Django 3.2.15 on 2022-08-29 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0002_order_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='amount',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
