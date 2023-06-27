from django.contrib import admin
from django.contrib.admin import ModelAdmin

from store.models import Book


@admin.register(Book)
class BookAdmin(ModelAdmin):
    list_filter = ('price',)
    list_display = ('__str__', 'id', 'name',
                    'price', 'author', 'owner')
    list_display_links = ('__str__',)
    search_fields = ('__str__',)
