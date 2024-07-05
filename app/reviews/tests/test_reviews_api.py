"""
Tests for reviews API.
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from reviews.models import Review
from reviews.serializers import ReviewSerializer
from reviews.tests.utils_for_tests import sample_category, sample_author, sample_book


REVIEWS_URL = reverse('reviews-api:review-list')


class PublicReviewApiTests(TestCase):
    """Test unauthenticated review API access."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email='test@example.com', password='testpass123')

    def test_retrieve_reviews(self):
        """Test retrieving a list of reviews."""
        category = sample_category()
        author = sample_author()
        book = sample_book(category=category, author=author)
        Review.objects.create(book=book, reviewer=self.user, content='Great book', rating=5)
        Review.objects.create(book=book, reviewer=self.user, content='Good book', rating=4)

        res = self.client.get(REVIEWS_URL)

        reviews = Review.objects.all().order_by('-id')
        serializer = ReviewSerializer(reviews, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        response_data = res.data
        expected_data = serializer.data

        # Sort lists by 'content' to ensure the order is the same
        response_data_sorted = sorted(response_data, key=lambda x: x['content'])
        expected_data_sorted = sorted(expected_data, key=lambda x: x['content'])

        self.assertEqual(response_data_sorted, expected_data_sorted)


class PrivateReviewApiTests(TestCase):
    """Test authenticated review API access."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email='test@example.com', password='testpass123')
        self.client.force_authenticate(self.user)
        self.category = sample_category()
        self.author = sample_author()
        self.book = sample_book(category=self.category, author=self.author)

    def test_create_review(self):
        """Test creating a review."""
        payload = {'book': self.book.id, 'reviewer': self.user.id, 'content': 'Amazing book', 'rating': 5}
        res = self.client.post(REVIEWS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        review = Review.objects.get(id=res.data['id'])
        self.assertEqual(review.book.id, payload['book'])
        self.assertEqual(review.reviewer.id, payload['reviewer'])
        self.assertEqual(review.content, payload['content'])
        self.assertEqual(review.rating, payload['rating'])
