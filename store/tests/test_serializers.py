from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg, F, ExpressionWrapper, FloatField
from django_filters.compat import TestCase

from store.models import Book, UserBookRelation
from store.serializers import BookSerializer


class BookSerializerTestCase(TestCase):

    def test_ok(self):
        user1 = User.objects.create(username='test_username1',
                                    first_name='Igor', last_name='Pampa')
        user2 = User.objects.create(username='test_username2')
        user3 = User.objects.create(username='test_username3')

        book1 = Book.objects.create(name='Testbook1', price='111.34',
                                    owner=user1)
        book2 = Book.objects.create(name='Testbook2', price='111.000',
                                    discount=0.5)

        UserBookRelation.objects.create(user=user1, book=book1,
                                        like=True, rate=5)
        UserBookRelation.objects.create(user=user2, book=book1,
                                        in_bookmarks=True, rate=5)
        UserBookRelation.objects.create(user=user3, book=book1,
                                        like=True, rate=4)

        UserBookRelation.objects.create(user=user1, book=book2,
                                        like=False, rate=4)
        UserBookRelation.objects.create(user=user2, book=book2,
                                        like=False, rate=3)
        UserBookRelation.objects.create(user=user3, book=book2,
                                        like=True)

        books = Book.objects.all() \
            .annotate(annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
                      rating=Avg('userbookrelation__rate'),
                      price_with_discount=ExpressionWrapper(
                          F('price') - (F('price') * F('discount')),
                          output_field=FloatField()),
                      owner_name=F('owner__username')) \
            .prefetch_related('readers') \
            .order_by('id')

        data = BookSerializer(books, many=True).data

        expected_data = [
            {
                'name': book1.name,
                'price': '111.34',
                'author': 'Unknown',
                'annotated_likes': 2,
                'rating': '4.67',
                'price_with_discount': '111.34',
                'owner_name': 'test_username1',
                'readers': [
                    {
                        'first_name': 'Igor',
                        'last_name': 'Pampa'
                    },
                    {
                        'first_name': '',
                        'last_name': ''
                    },
                    {
                        'first_name': '',
                        'last_name': ''
                    }
                ]
            },
            {
                'name': book2.name,
                'price': '111.00',
                'author': 'Unknown',
                'annotated_likes': 1,
                'rating': '3.50',
                'price_with_discount': '55.50',
                'owner_name': None,
                'readers': [
                    {
                        'first_name': 'Igor',
                        'last_name': 'Pampa'
                    },
                    {
                        'first_name': '',
                        'last_name': ''
                    },
                    {
                        'first_name': '',
                        'last_name': ''
                    }
                ]
            },
        ]
        self.assertEqual(expected_data, data)
