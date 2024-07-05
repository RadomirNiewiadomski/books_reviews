"""
Database models for reviews.
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
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books')
    average_rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True, upload_to=book_image_file_path)

    def __str__(self):
        return self.title

    def update_average_rating(self):
        """Update the average rating for the book based on reviews."""
        reviews = self.review_set.all()
        total_rating = sum(review.rating for review in reviews)
        self.average_rating = total_rating / reviews.count() if reviews.count() > 0 else 0
        self.save()

    def short_description(self):
        return self.description.split('.')[0] + '...'


class Review(models.Model):
    RATING_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reviewer.name}'s review of {self.book.title}"

    def save(self, *args, **kwargs):
        """Override save method to update book's average rating."""
        super().save(*args, **kwargs)
        self.book.update_average_rating()
