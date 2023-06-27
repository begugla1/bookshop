from django.contrib.auth.models import User
from django.db import models


class Book(models.Model):
    name = models.CharField('Name', max_length=255)
    price = models.DecimalField('Price', max_digits=9, decimal_places=2)
    author = models.CharField('Author', max_length=255, default='Unknown')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL,
                              null=True, verbose_name="Owner")

    def __str__(self):
        return f'{self.name} with price {self.price:.2f}'
