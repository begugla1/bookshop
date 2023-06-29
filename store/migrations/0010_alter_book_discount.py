# Generated by Django 4.2.2 on 2023-06-29 13:33

from decimal import Decimal
from django.db import migrations, models
import store.validators


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_book_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=3, validators=[store.validators.discount_validator], verbose_name='Discount'),
        ),
    ]
