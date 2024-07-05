"""
Django admin customization.
"""
from django.contrib import admin

from reviews.models import Category, Author, Book, Review


admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Review)
