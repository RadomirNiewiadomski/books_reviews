"""
Tests for models.
"""
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model
from reviews.models import (
    Category,
    Author,
    Book,
    Review,
    book_image_file_path,
)

class ModelTest(TestCase):
    """Test models."""

    def setUp(self):
        self.category = Category.objects.create(name='Biography')
        self.author = Author.objects.create(
            name='John West',
            description='An author of many books.'
        )
        self.book = Book.objects.create(
            title='Some title',
            description='Book about teenagers life',
            category=self.category,
        )
        self.book.author.add(self.author)
        self.user1 = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123',
            name='Mark Don'
        )
        self.user2 = get_user_model().objects.create_user(
            email='test2@example.com',
            password='test2pass123',
            name='Second User'
        )

    def test_create_category(self):
        """Test creating a category is successful."""
        category = Category.objects.create(name='Science Fiction')
        self.assertEqual(str(category), category.name)

    def test_create_author(self):
        """Test creating an author is successful."""
        author = Author.objects.create(
            name='Jane Doe',
            description='An author of science fiction books.'
        )
        self.assertEqual(str(author), author.name)

    def test_create_book(self):
        """Test creating a book is successful."""
        book = Book.objects.create(
            title='New Book Title',
            description='A new book description.',
            category=self.category,
        )
        book.author.add(self.author)
        self.assertEqual(str(book), book.title)

    def test_create_review(self):
        """Test creating a review is successful."""
        review = Review.objects.create(
            book=self.book,
            reviewer=self.user1,
            content='Fantastic book',
            rating=5
        )
        self.assertEqual(str(review), f"{review.reviewer.name}'s review of {review.book.title}")

    def test_average_rating(self):
        """Test calculating average rating is successful."""
        Review.objects.create(
            book=self.book,
            reviewer=self.user1,
            content='Great book',
            rating=5
        )
        Review.objects.create(
            book=self.book,
            reviewer=self.user2,
            content='Good book',
            rating=3
        )
        self.book.refresh_from_db()
        self.assertEqual(self.book.average_rating, 4.0)

    @patch('reviews.models.uuid.uuid4')
    def test_book_file_name_uuid(self, mock_uuid):
        """Test generating image path."""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = book_image_file_path(None, 'example.jpg')
        self.assertEqual(file_path, f'uploads/book/{uuid}.jpg')
