from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book
from store.serializers import BookSerializer


class BooksApiTestCase(APITestCase):

    def setUp(self):
        self.book1 = Book.objects.create(name='Testbook1 John', price='111.34')
        self.book2 = Book.objects.create(name='Testbook2', price='111.00')
        self.book3 = Book.objects.create(name='Testbook3', price='0.23',
                                         author='Mike')
        self.book4 = Book.objects.create(name='Testbook4', price='111213.00',
                                         author='John')
        self.url = reverse_lazy('book-list')

    def test_get_1(self):
        response = self.client.get(self.url)
        serializer_data = BookSerializer(
            [self.book1, self.book2,
             self.book3, self.book4],
            many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        response = self.client.get(self.url, data={'search': 'John'})
        serializer_data = BookSerializer([
            self.book1, self.book4
        ], many=True).data

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        response = self.client.get(self.url, data={'price': '0.23'})
        serializer_data = BookSerializer([self.book3],
                                         many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_ordering(self):
        response = self.client.get(self.url, data={'ordering': 'price'})
        serializer_data = BookSerializer([
            self.book3, self.book2,
            self.book1, self.book4
        ], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
