import json
from decimal import Decimal

from django.contrib.auth.models import User
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book
from store.serializers import BookSerializer


class BooksApiTestCase(APITestCase):

    def setUp(self):
        self.test_user = User.objects.create(username="test_username", password="test_password")
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

    def test_create(self):
        self.assertEqual(4, Book.objects.all().count())
        data = {
            "name": "Scooby Do 2",
            "price": "123.12",
            "author": "Shaggy"
        }
        json_data = json.dumps(data)
        self.client.force_login(self.test_user)
        response = self.client.post(self.url,
                                    data=json_data,
                                    content_type="application/json")

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(5, Book.objects.all().count())

    def test_update(self):
        url = reverse_lazy('book-detail', args=(self.book1.id,))
        self.assertEqual(4, Book.objects.all().count())
        data = {
            "name": self.book1.name,
            "price": 990000,
            "author": self.book1.author
        }
        json_data = json.dumps(data)
        self.client.force_login(self.test_user)
        response = self.client.put(url,
                                   data=json_data,
                                   content_type="application/json")

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(4, Book.objects.all().count())
        self.book1.refresh_from_db()
        self.assertEqual(Decimal(990000), self.book1.price)

    def test_delete(self):
        url = reverse_lazy('book-detail', args=(self.book1.id,))
        self.assertEqual(4, Book.objects.all().count())
        self.client.force_login(self.test_user)
        response = self.client.delete(url)
        self.assertEqual(204, response.status_code)
        self.assertEqual(3, Book.objects.all().count())

    def test_get_detail(self):
        url = reverse_lazy('book-detail', args=(self.book1.id,))
        json_data = {
            "id": self.book1.id,
            "name": self.book1.name,
            "price": self.book1.price,
            "author": self.book1.author
        }
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(json_data, response.data)
