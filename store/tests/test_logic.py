from django.contrib.auth.models import User
from django.test import TestCase

from store.logic import set_rating
from store.models import UserBookRelation, Book


class SetRatingTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username='test_username1',
                                    first_name='Igor', last_name='Pampa')
        user2 = User.objects.create(username='test_username2')
        user3 = User.objects.create(username='test_username3')

        self.book1 = Book.objects.create(name='Testbook1', price='111.34',
                                         owner=user1)
        UserBookRelation.objects.create(user=user1, book=self.book1,
                                        like=True, rate=5)
        UserBookRelation.objects.create(user=user2, book=self.book1,
                                        in_bookmarks=True, rate=5)
        self.user_book_3 = UserBookRelation.objects.create(user=user3, book=self.book1,
                                                           like=True, rate=4)

    def test_ok(self):
        set_rating(self.book1)
        self.book1.refresh_from_db()
        self.assertEqual('4.67', str(self.book1.rating))

    def test_save(self):
        self.user_book_3.rate = 5
        result = self.user_book_3.save()
        self.book1.refresh_from_db()
        self.assertEqual('5.00', str(self.book1.rating))
        self.assertEqual('cached_field_was_not_used', result)
        self.user_book_3.rate = 5
        result = self.user_book_3.save()
        self.assertEqual(None, result)
