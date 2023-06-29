from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django_filters.compat import TestCase

from store.models import Book, UserBookRelation
from store.serializers import BookSerializer


class BookSerializerTestCase(TestCase):

    def test_ok(self):
        user1 = User.objects.create(username='test_usdeddr1')
        user2 = User.objects.create(username='test_usddedr2')
        user3 = User.objects.create(username='test_usddedr3')

        book1 = Book.objects.create(name='Testbook1', price='111.34')
        book2 = Book.objects.create(name='Testbook2', price='111.000')

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

        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')) \
            .order_by('id')
        data = BookSerializer(books, many=True).data

        expected_data = [
            {
                'name': book1.name,
                'price': '111.34',
                'author': 'Unknown',
                'likes_count': 2,
                'annotated_likes': 2,
                'rating': '4.67'
            },
            {
                'name': book2.name,
                'price': '111.00',
                'author': 'Unknown',
                'likes_count': 1,
                'annotated_likes': 1,
                'rating': '3.50'
            },
        ]
        self.assertEqual(expected_data, data)
