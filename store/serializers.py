from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from store.models import Book, UserBookRelation


class BookSerializer(ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    # annotated_likes = serializers.IntegerField()

    class Meta:
        model = Book
        fields = ('id', 'name', 'price', 'author',
                  'likes_count')

    def get_likes_count(self, instance):
        return UserBookRelation.objects.filter(book=instance, like=True).count()


class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ('book', 'like', 'in_bookmarks',
                  'rate', 'review')
