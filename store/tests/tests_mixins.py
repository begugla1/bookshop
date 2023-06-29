from django.contrib.auth.models import User
from django.urls import reverse_lazy

from store.models import Book, UserBookRelation


class ApiStoreTestsMixin:
    def setUp(self):
        self.test_user = User.objects.create(username="test_username")
        self.test_user2 = User.objects.create(username='test_username2')
        self.test_user3 = User.objects.create(username="test_username3",
                                              is_staff=True)
        self.book1 = Book.objects.create(name='Testbook1 John', price='111.34',
                                         owner=self.test_user, discount=0.37)
        self.book2 = Book.objects.create(name='Testbook2', price='111.00')
        self.book3 = Book.objects.create(name='Testbook3', price='0.23',
                                         author='Mike')
        self.book4 = Book.objects.create(name='Testbook4', price='111213.00',
                                         author='John')
        UserBookRelation.objects.create(user=self.test_user, book=self.book1,
                                        like=True, rate=5)
        self.url = reverse_lazy('book-list')
