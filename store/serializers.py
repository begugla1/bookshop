from django.contrib.auth.models import User
from rest_framework import serializers
from store.models import Book, UserBookRelation


class BookReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class BookSerializer(serializers.ModelSerializer):
    annotated_likes = serializers.IntegerField(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2,
                                      read_only=True)
    price_with_discount = serializers.DecimalField(read_only=True, max_digits=9,
                                                   decimal_places=2)
    owner_name = serializers.CharField(read_only=True)
    readers = BookReaderSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ('name', 'price', 'author', 'annotated_likes',
                  'rating', 'price_with_discount', 'owner_name',
                  'readers')


class UserBookRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ('book', 'like', 'in_bookmarks',
                  'rate', 'review')
