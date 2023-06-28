from django.contrib import admin
from django.contrib.admin import ModelAdmin

from store.models import Book, UserBookRelation


@admin.register(Book)
class BookAdmin(ModelAdmin):
    list_filter = ('price',)
    list_display = ('id', 'name', 'price',
                    'author', 'owner')
    list_display_links = ('name',)
    search_fields = ('__str__',)


@admin.register(UserBookRelation)
class UserBookRelationAdmin(ModelAdmin):
    list_filter = ('user', 'rate',
                   'in_bookmarks', 'like')
    list_display = ('__str__', 'user', 'book',
                    'rate', 'in_bookmarks', 'like')
    list_display_links = ('__str__',)
    search_fields = ('user', 'book')
    list_editable = ('in_bookmarks', 'like',
                     'rate')
