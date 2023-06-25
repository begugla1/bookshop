from django.db import models


class Book(models.Model):
    name = models.CharField('Name', max_length=255)
    price = models.DecimalField('Price', max_digits=9, decimal_places=2)
    author = models.CharField('Author', max_length=255, default='Unknown')

    def __str__(self):
        return f'{self.name} with price {self.price:.2f}'
