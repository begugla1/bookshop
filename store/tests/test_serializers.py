from unittest import TestCase

from django.contrib.auth.models import User
from django.db.models import Count, Case, When

from store.models import Book, UserBookRelation
from store.serializers import BookSerializer


class BookSerializerTestCase(TestCase):

    def test_ok(self):
        user1 = User.objects.create(username='user1')
        user2 = User.objects.create(username='user2')
        user3 = User.objects.create(username='user3')

        book1 = Book.objects.create(name='Testbook1', price='111.34')
        book2 = Book.objects.create(name='Testbook2', price='111.000')

        UserBookRelation.objects.create(user=user1, book=book1,
                                        like=True)
        UserBookRelation.objects.create(user=user2, book=book1,
                                        in_bookmarks=True)
        UserBookRelation.objects.create(user=user3, book=book1,
                                        like=True, in_bookmarks=True)

        UserBookRelation.objects.create(user=user1, book=book2,
                                        like=False)
        UserBookRelation.objects.create(user=user2, book=book2,
                                        like=False)
        UserBookRelation.objects.create(user=user3, book=book2,
                                        like=True)

        # books = Book.objects.all().annotate(
        #     annotated_likes=Count(Case(When(userbookrelation__like=True, then=1)))) \
        #     .order_by('id')
        data = BookSerializer([book1, book2], many=True).data

        expected_data = [
            {
                'id': book1.id,
                'name': book1.name,
                'price': '111.34',
                'author': 'Unknown',
                'likes_count': 2,
            },
            {
                'id': book2.id,
                'name': book2.name,
                'price': '111.00',
                'author': 'Unknown',
                'likes_count': 1,
            },
        ]
        self.assertEqual(expected_data, data)
