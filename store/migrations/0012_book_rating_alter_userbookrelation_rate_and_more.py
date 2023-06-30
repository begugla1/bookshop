# Generated by Django 4.2.2 on 2023-06-30 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_alter_book_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='rating',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True, verbose_name='Rating'),
        ),
        migrations.AlterField(
            model_name='userbookrelation',
            name='rate',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Bad'), (2, 'Ok'), (3, 'Good'), (4, 'Amazing'), (5, 'Incredible')], null=True, verbose_name='Rate'),
        ),
        migrations.AlterField(
            model_name='userbookrelation',
            name='review',
            field=models.TextField(blank=True, null=True, verbose_name='Review'),
        ),
    ]
