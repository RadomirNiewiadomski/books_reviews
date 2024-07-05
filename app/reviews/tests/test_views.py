"""
Tests for views.
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from reviews.models import Book, Review, Author, Category
from reviews.tests.utils_for_tests import sample_category, sample_author, sample_book


User = get_user_model()


class BookListViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = sample_category(name='Science Fiction')
        self.author = sample_author(name='Jane Doe')
        self.book = sample_book(
            title='A Sci-Fi Book', category=self.category, author=self.author
        )

    def test_book_list_view(self):
        response = self.client.get(reverse('reviews:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book.title)

    def test_book_list_view_with_search(self):
        response = self.client.get(reverse('reviews:index'), {'q': 'Sci-Fi'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book.title)

    def test_book_list_view_with_category_filter(self):
        response = self.client.get(reverse('reviews:index'), {'category': self.category.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book.title)


class BookDetailViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = sample_category(name='Science Fiction')
        self.author = sample_author(name='Jane Doe')
        self.book = sample_book(
            title='A Sci-Fi Book', category=self.category, author=self.author
        )
        self.user = User.objects.create_user(email='test@example.com', password='testpass123', name='Test User')

    def test_book_detail_view(self):
        response = self.client.get(reverse('reviews:book_detail', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book.title)

    def test_book_detail_view_with_reviews(self):
        Review.objects.create(book=self.book, reviewer=self.user, content='Great book', rating=5)
        response = self.client.get(reverse('reviews:book_detail', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Great book')

    def test_book_detail_view_pagination(self):
        for i in range(5):
            Review.objects.create(book=self.book, reviewer=self.user, content=f'Review {i}', rating=5)
        response = self.client.get(reverse('reviews:book_detail', args=[self.book.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Review 4')
        self.assertContains(response, 'Review 3')
        self.assertContains(response, 'Review 2')
        self.assertNotContains(response, 'Review 1')
        self.assertNotContains(response, 'Review 0')


class AddBookViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='admin@example.com', password='adminpass123', name='Admin User', is_staff=True
        )
        self.category = sample_category(name='Science Fiction')
        self.author = sample_author(name='Jane Doe')

    def test_add_book_view(self):
        self.client.login(email='admin@example.com', password='adminpass123')
        response = self.client.get(reverse('reviews:add_book'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('reviews:add_book'),
            {
                'title': 'New Sci-Fi Book',
                'description': 'A new sci-fi book description.',
                'category': self.category.id,
                'author': self.author.id,
            },
        )
        self.assertEqual(response.status_code, 302)

        new_book = Book.objects.get(title='New Sci-Fi Book')
        self.assertEqual(new_book.description, 'A new sci-fi book description.')


class AddAuthorViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='admin@example.com', password='adminpass123', name='Admin User', is_staff=True
        )

    def test_add_author_view(self):
        self.client.login(email='admin@example.com', password='adminpass123')
        response = self.client.get(reverse('reviews:add_author'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('reviews:add_author'), {'name': 'New Author', 'description': 'An author description.'}
        )
        self.assertEqual(response.status_code, 302)

        new_author = Author.objects.get(name='New Author')
        self.assertEqual(new_author.description, 'An author description.')


class AddCategoryViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='admin@example.com', password='adminpass123', name='Admin User', is_staff=True
        )

    def test_add_category_view(self):
        self.client.login(email='admin@example.com', password='adminpass123')
        response = self.client.get(reverse('reviews:add_category'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('reviews:add_category'), {'name': 'New Category'})
        self.assertEqual(response.status_code, 302)

        new_category = Category.objects.get(name='New Category')
        self.assertEqual(str(new_category), 'New Category')


class AddReviewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@example.com', password='testpass123', name='Test User'
        )
        self.category = sample_category(name='Science Fiction')
        self.author = sample_author(name='Jane Doe')
        self.book = sample_book(
            title='A Sci-Fi Book', category=self.category, author=self.author
        )

    def test_add_review(self):
        self.client.login(email='test@example.com', password='testpass123')
        response = self.client.post(
            reverse('reviews:add_review', args=[self.book.id]),
            {'content': 'Amazing book', 'rating': 5},
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)

        new_review = Review.objects.get(content='Amazing book')
        self.assertEqual(new_review.rating, 5)
        self.assertEqual(new_review.book, self.book)
        self.assertEqual(new_review.reviewer, self.user)

    def test_add_review_already_reviewed(self):
        self.client.login(email='test@example.com', password='testpass123')
        Review.objects.create(book=self.book, reviewer=self.user, content='Great book', rating=5)

        response = self.client.post(
            reverse('reviews:add_review', args=[self.book.id]),
            {'content': 'Another review', 'rating': 4},
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': False, 'message': 'You have already reviewed this book.'})

    def test_add_review_missing_content_or_rating(self):
        self.client.login(email='test@example.com', password='testpass123')

        response = self.client.post(
            reverse('reviews:add_review', args=[self.book.id]),
            {'content': '', 'rating': 5},
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': False, 'message': 'Content and rating are required.'})

        response = self.client.post(
            reverse('reviews:add_review', args=[self.book.id]),
            {'content': 'Great book', 'rating': ''},
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': False, 'message': 'Content and rating are required.'})
