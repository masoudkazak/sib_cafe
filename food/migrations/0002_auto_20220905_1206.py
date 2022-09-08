# Generated by Django 3.2.15 on 2022-09-05 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='days',
            field=models.IntegerField(choices=[(0, 'Everyday'), (1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Saturday'), (5, 'Sunday')], default=0, verbose_name='days'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.IntegerField(choices=[(0, 'Order'), (1, 'Cancel'), (2, 'Accept'), (3, 'Paid'), (4, 'Debt')], default=0, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='review',
            name='value',
            field=models.IntegerField(choices=[(0, 'Zero Point'), (1, 'One Point'), (2, 'Two Points'), (3, 'Three Points'), (4, 'Four Points'), (5, 'Five Points')], verbose_name='value'),
        ),
    ]