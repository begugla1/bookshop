import json
from decimal import Decimal

from django.db.models import Count, Case, When, Avg, ExpressionWrapper, F, FloatField
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book, UserBookRelation
from store.serializers import BookSerializer
from .tests_mixins import ApiStoreTestsMixin


class BooksApiTestCase(ApiStoreTestsMixin, APITestCase):

    def test_get(self):
        response = self.client.get(self.url)
        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate'),
            price_with_discount=ExpressionWrapper(
                F('price') - (F('price') * F('discount')),
                output_field=FloatField())) \
            .order_by('id')
        serializer_data = BookSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(serializer_data[0]['rating'], '5.00')
        self.assertEqual(serializer_data[0]['annotated_likes'], 1)
        self.assertEqual(serializer_data[0]['likes_count'], 1)
        self.assertEqual(serializer_data[0]['price_with_discount'], '70.14')

    def test_get_search(self):
        response = self.client.get(self.url, data={'search': 'John'})
        books = Book.objects.filter(id__in=[self.book1.id, self.book4.id]).annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate'),
            price_with_discount=ExpressionWrapper(
                F('price') - (F('price') * F('discount')),
                output_field=FloatField())) \
            .order_by('id')
        serializer_data = BookSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        response = self.client.get(self.url, data={'price': '0.23'})
        books = Book.objects.filter(id__in=[self.book3.id]).annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate'),
            price_with_discount=ExpressionWrapper(
                F('price') - (F('price') * F('discount')),
                output_field=FloatField())) \
            .order_by('id')
        serializer_data = BookSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_ordering(self):
        response = self.client.get(self.url, data={'ordering': 'price'})
        books = Book.objects.all().annotate(
            annotated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate'),
            price_with_discount=ExpressionWrapper(
                F('price') - (F('price') * F('discount')),
                output_field=FloatField())) \
            .order_by('price')
        serializer_data = BookSerializer(books, many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(4, Book.objects.all().count())
        data = {
            "name": "Scooby Do 2",
            "price": "123.12",
            "author": "Shaggy",
            "likes_count": 0,
            "annotated_likes": 0,
            "rating": None
        }
        json_data = json.dumps(data)
        self.client.force_login(self.test_user)
        response = self.client.post(self.url,
                                    data=json_data,
                                    content_type="application/json")

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(5, Book.objects.all().count())
        self.assertEqual(self.test_user, Book.objects.last().owner)

    def test_delete(self):
        url = reverse_lazy('book-detail', args=(self.book1.id,))
        self.assertEqual(4, Book.objects.all().count())
        self.client.force_login(self.test_user)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(3, Book.objects.all().count())

    def test_delete_not_owner(self):
        url = reverse_lazy('book-detail', args=(self.book1.id,))
        self.assertEqual(4, Book.objects.all().count())
        self.client.force_login(self.test_user2)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(4, Book.objects.all().count())

    def test_get_detail(self):
        url = reverse_lazy('book-detail', args=(self.book1.id,))
        json_data = {
            "name": self.book1.name,
            "price": self.book1.price,
            "author": self.book1.author,
            "likes_count": 1,
            "annotated_likes": 1,
            "rating": "5.00",
            "price_with_discount": '70.14'
        }
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(json_data, response.data)

    def test_update(self):
        url = reverse_lazy('book-detail', args=(self.book1.id,))
        self.assertEqual(4, Book.objects.all().count())
        data = {
            "name": self.book1.name,
            "price": 990000
        }
        json_data = json.dumps(data)
        self.client.force_login(self.test_user)
        response = self.client.put(url,
                                   data=json_data,
                                   content_type="application/json")

        self.assertEqual(status.HTTP_200_OK, response.status_code,
                         response.data)
        self.assertEqual(4, Book.objects.all().count())
        self.book1.refresh_from_db()
        self.assertEqual(Decimal(990000), self.book1.price)

    def test_update_not_owner(self):
        url = reverse_lazy('book-detail', args=(self.book1.id,))
        self.assertEqual(4, Book.objects.all().count())
        data = {
            "name": self.book1.name,
            "price": 990000,
            "author": self.book1.author,
            "likes_count": 0,
            "annotated_likes": 0,
            "rating": None
        }
        json_data = json.dumps(data)
        self.client.force_login(self.test_user2)
        response = self.client.put(url,
                                   data=json_data,
                                   content_type="application/json")
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.book1.refresh_from_db()
        self.assertEqual(Decimal('111.34'), self.book1.price)

    def test_update_not_owner_but_staff(self):
        url = reverse_lazy('book-detail', args=(self.book1.id,))
        self.assertEqual(4, Book.objects.all().count())
        data = {
            "name": self.book1.name,
            "price": 990000,
            "author": self.book1.author,
            "likes_count": 0,
            "annotated_likes": 0,
            "rating": None
        }
        json_data = json.dumps(data)
        self.client.force_login(self.test_user3)
        response = self.client.put(url,
                                   data=json_data,
                                   content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book1.refresh_from_db()
        self.assertEqual(990000, self.book1.price)


class BooksRelationTestCase(ApiStoreTestsMixin, APITestCase):

    def test_like_and_in_bookmarks(self):
        self.url = reverse_lazy('userbookrelation-detail', args=(self.book1.id,))

        data = {
            "like": True
        }
        json_data = json.dumps(data)

        self.client.force_login(self.test_user)
        response = self.client.patch(self.url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.test_user,
                                                book=self.book1)
        self.assertTrue(relation.like)

        new_data = {
            "in_bookmarks": True
        }
        new_json_data = json.dumps(new_data)
        new_response = self.client.patch(self.url, data=new_json_data,
                                         content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, new_response.status_code)
        relation.refresh_from_db()
        self.assertTrue(relation.in_bookmarks)

    def test_rate(self):
        self.url = reverse_lazy('userbookrelation-detail', args=(self.book1.id,))

        data = {
            "rate": 5
        }
        json_data = json.dumps(data)

        self.client.force_login(self.test_user)
        response = self.client.patch(self.url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.test_user,
                                                book=self.book1)
        self.assertEqual(5, relation.rate)

        new_data = {
            "rate": 2
        }
        new_json_data = json.dumps(new_data)
        new_response = self.client.patch(self.url, data=new_json_data,
                                         content_type='application/json')

        self.assertEqual(status.HTTP_200_OK, new_response.status_code)
        relation.refresh_from_db()
        self.assertTrue(2, relation.rate)

    def test_rate_wrong(self):
        self.url = reverse_lazy('userbookrelation-detail', args=(self.book2.id,))

        data = {
            "rate": 111
        }
        json_data = json.dumps(data)

        self.client.force_login(self.test_user)
        response = self.client.patch(self.url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code,
                         response.data)
        relation = UserBookRelation.objects.get(user=self.test_user,
                                                book=self.book2)
        self.assertEqual(None, relation.rate)

    def test_review(self):
        self.url = reverse_lazy('userbookrelation-detail', args=(self.book1.id,))

        data = {
            "review": 'It\'s a very good book!'
        }
        json_data = json.dumps(data)

        self.client.force_login(self.test_user)
        response = self.client.patch(self.url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        relation = UserBookRelation.objects.get(user=self.test_user,
                                                book=self.book1)
        self.assertEqual(data['review'], relation.review)
