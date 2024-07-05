"""
Sample utils to import.
"""
from reviews.models import Category, Author, Book


def sample_category(name='Science Fiction'):
    """Create and return a sample category."""
    return Category.objects.create(name=name)


def sample_author(name='Jane Doe'):
    """Create and return a sample author."""
    return Author.objects.create(name=name, description='A science fiction author')


def sample_book(category, author, **params):
    """Create and return a sample book."""
    defaults = {
        'title': 'Sample Book',
        'description': 'Sample book description.',
        'category': category,
        'author': author,
    }
    defaults.update(params)

    return Book.objects.create(**defaults)
