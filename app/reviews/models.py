"""
Database models.
"""
import uuid
import os

from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import User


def book_image_file_path(instance, filename):
    """Generate file path for new book image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'book', filename)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ManyToManyField(Author)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    average_rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True,
                              upload_to=book_image_file_path)
    
    def __str__(self):
        return self.title

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.reviewer.name}'s review of {self.book.title}"