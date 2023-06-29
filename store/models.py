from django.contrib.auth.models import User
from django.db import models
from decimal import Decimal

from store.validators import discount_validator


class Book(models.Model):
    name = models.CharField('Name', max_length=255)
    price = models.DecimalField('Price', max_digits=9, decimal_places=2)
    author = models.CharField('Author', max_length=255, default='Unknown')
    owner = models.ForeignKey(User, on_delete=models.SET_NULL,
                              null=True, verbose_name="Owner",
                              related_name='my_books', blank=True)
    readers = models.ManyToManyField(User, through='UserBookRelation',
                                     verbose_name='Readers',
                                     related_name='books')
    discount = models.DecimalField('Discount', max_digits=3, decimal_places=2,
                                   default=Decimal(0), validators=[discount_validator])

    def __str__(self):
        return self.name


class UserBookRelation(models.Model):
    RATE_CHOICES = (
        (1, 'Bad'),
        (2, 'Ok'),
        (3, 'Good'),
        (4, 'Amazing'),
        (5, 'Incredible')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name="Owner")
    book = models.ForeignKey(Book, on_delete=models.CASCADE,
                             verbose_name='Book')
    like = models.BooleanField('Like', default=False)
    in_bookmarks = models.BooleanField('In bookmarks', default=False)
    rate = models.PositiveSmallIntegerField('Rate', choices=RATE_CHOICES,
                                            null=True, blank=True)
    review = models.TextField('Review', null=True, blank=True)

    def __str__(self):
        return f'Relation of {self.user} to {self.book}'
