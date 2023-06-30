from django.contrib.auth.models import User
from django.db.models import Count, Case, When, F, ExpressionWrapper, FloatField, Prefetch
from django_filters.compat import TestCase

from store.models import Book, UserBookRelation
from store.serializers import BookSerializer


class BookSerializerTestCase(TestCase):

    def test_ok(self):
        self.user1 = User.objects.create(username='test_username1',
                                         first_name='Igor', last_name='Pampa')
        self.user2 = User.objects.create(username='test_username2')
        self.user3 = User.objects.create(username='test_username3')

        self.book1 = Book.objects.create(name='Testbook1', price='111.34',
                                         owner=self.user1)
        self.book2 = Book.objects.create(name='Testbook2', price='111.000',
                                         discount=0.5)

        UserBookRelation.objects.create(user=self.user1, book=self.book1,
                                        like=True, rate=5)
        UserBookRelation.objects.create(user=self.user2, book=self.book1,
                                        in_bookmarks=True, rate=5)
        user_book_relation_3 = UserBookRelation.objects.create(user=self.user3, book=self.book1,
                                                               like=True, rate=3)
        user_book_relation_3.rate = 4
        user_book_relation_3.save()

        UserBookRelation.objects.create(user=self.user1, book=self.book2,
                                        like=False, rate=4)
        UserBookRelation.objects.create(user=self.user2, book=self.book2,
                                        like=False, rate=3)
        UserBookRelation.objects.create(user=self.user3, book=self.book2,
                                        like=True)

        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            price_with_discount=ExpressionWrapper(F('price') - (F('price') * F('discount')),
                                                  output_field=FloatField()),
            owner_name=F('owner__username')).prefetch_related(
            Prefetch('readers', queryset=User.objects.all().only('first_name', 'last_name'))) \
            .order_by('id')

        data = BookSerializer(books, many=True).data

        expected_data = [
            {
                'name': self.book1.name,
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
                'name': self.book2.name,
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
