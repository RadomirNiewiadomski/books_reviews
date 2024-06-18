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
    
    def test_create_category(self):
        """Test creating a category is successful."""
        category = Category.objects.create(name='Biography')

        self.assertEqual(str(category), category.name)

    def test_create_author(self):
        """Test creating an author is successful."""
        author = Author.objects.create(
            name='John West',
            description='An author of many books.'
        )

        self.assertEqual(str(author), author.name)

    def test_create_book(self):
        """Test creating a book is successful."""
        category = Category.objects.create(name='Biography')
        author = Author.objects.create(
            name='John West',
            description='An author of many books.'
        )

        book = Book.objects.create(
            title='Some title',
            description='Book about teenagers life',
            category=category,
        )
        book.author.add(author)

        self.assertEqual(str(book), book.title)

    def test_create_review(self):
        """Test creating a review is successful."""
        category = Category.objects.create(name='Biography')
        author = Author.objects.create(
            name='John West',
            description='An author of many books.'
        )
        book = Book.objects.create(
            title='Some title',
            description='Book about teenagers life',
            category=category,
        )
        book.author.add(author)

        user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123',
            name='Mark Don'
        )

        review = Review.objects.create(
            book=book,
            reviewer=user,
            content='Fantastic book',
            rating=5
        )

        self.assertEqual(str(review), f"{review.reviewer.name}'s review of {review.book.title}")

    @patch('reviews.models.uuid.uuid4')
    def test_book_file_name_uuid(self, mock_uuid):
        """Test generating image path."""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = book_image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/book/{uuid}.jpg')
