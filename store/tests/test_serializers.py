from unittest import TestCase

from store.models import Book
from store.serializers import BookSerializer


class BookSerializerTestCase(TestCase):

    def test_ok(self):
        book1 = Book.objects.create(name='Testbook1', price='111.34')
        book2 = Book.objects.create(name='Testbook2', price='111.000')
        data = BookSerializer([book1, book2], many=True).data
        expected_data = [
            {
                'id': book1.id,
                'name': book1.name,
                'price': '111.34',
                'author': 'Unknown',
                'owner': None,
                'readers': []
            },
            {
                'id': book2.id,
                'name': book2.name,
                'price': '111.00',
                'author': 'Unknown',
                'owner': None,
                'readers': []
            },
        ]
        self.assertEqual(expected_data, data)

