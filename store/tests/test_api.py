from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book
from store.serializers import BookSerializer


class BooksApiTestCase(APITestCase):

    def test_get(self):
        book1 = Book.objects.create(name='Testbook1', price='111.34')
        book2 = Book.objects.create(name='Testbook2', price='111.000')
        url = reverse_lazy('book-list')
        response = self.client.get(url)
        serializer_data = BookSerializer(
            [book1, book2],
            many=True).data
        self.assertEqual(
            status.HTTP_200_OK,
            response.status_code
        )
        self.assertEqual(
            serializer_data,
            response.data
        )

