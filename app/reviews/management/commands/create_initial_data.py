from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from reviews.models import Category, Author, Book, Review

class Command(BaseCommand):
    """Command to add initial data to database if there is no data in db (in DEV mode)."""

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Checking for existing initial data...'))

        # Check and create categories
        if not Category.objects.exists():
            self.stdout.write(self.style.SUCCESS('Creating categories...'))
            category1 = Category.objects.create(name='Biography')
            category2 = Category.objects.create(name='Science Fiction')
            category3 = Category.objects.create(name='Fantasy')
        else:
            self.stdout.write(self.style.SUCCESS('Categories already exist.'))

        # Check and create authors
        if not Author.objects.exists():
            self.stdout.write(self.style.SUCCESS('Creating authors...'))
            author1 = Author.objects.create(name='John West', description='An author of many books.')
            author2 = Author.objects.create(name='Jane Doe', description='An author of science fiction books.')
            author3 = Author.objects.create(name='Alice Smith', description='An author of fantasy novels.')
        else:
            self.stdout.write(self.style.SUCCESS('Authors already exist.'))

        # Check and create books
        if not Book.objects.exists():
            self.stdout.write(self.style.SUCCESS('Creating books...'))
            book1 = Book.objects.create(
                title='Life of John',
                description='A biography of John West.',
                category=Category.objects.get(name='Biography')
            )
            book1.author.add(Author.objects.get(name='John West'))

            book2 = Book.objects.create(
                title='The Future',
                description='A science fiction novel by Jane Doe.',
                category=Category.objects.get(name='Science Fiction')
            )
            book2.author.add(Author.objects.get(name='Jane Doe'))

            book3 = Book.objects.create(
                title='Magic World',
                description='A fantasy novel by Alice Smith.',
                category=Category.objects.get(name='Fantasy')
            )
            book3.author.add(Author.objects.get(name='Alice Smith'))
        else:
            self.stdout.write(self.style.SUCCESS('Books already exist.'))

        # Check and create users
        User = get_user_model()
        if not User.objects.filter(email='user1@example.com').exists():
            self.stdout.write(self.style.SUCCESS('Creating users...'))
            user1 = User.objects.create_user(email='user1@example.com', password='password123', name='User One')
        else:
            self.stdout.write(self.style.SUCCESS('User user1@example.com already exists.'))

        if not User.objects.filter(email='user2@example.com').exists():
            user2 = User.objects.create_user(email='user2@example.com', password='password123', name='User Two')
        else:
            self.stdout.write(self.style.SUCCESS('User user2@example.com already exists.'))

        # Check and create reviews
        if not Review.objects.exists():
            self.stdout.write(self.style.SUCCESS('Creating reviews...'))
            book1 = Book.objects.get(title='Life of John')
            book2 = Book.objects.get(title='The Future')
            book3 = Book.objects.get(title='Magic World')

            user1 = User.objects.get(email='user1@example.com')
            user2 = User.objects.get(email='user2@example.com')

            Review.objects.create(book=book1, reviewer=user1, content='An inspiring biography.', rating=5)
            Review.objects.create(book=book2, reviewer=user2, content='A fascinating sci-fi novel.', rating=4)
            Review.objects.create(book=book3, reviewer=user1, content='An enchanting fantasy story.', rating=5)
        else:
            self.stdout.write(self.style.SUCCESS('Reviews already exist.'))

        self.stdout.write(self.style.SUCCESS('Initial data check and creation completed successfully.'))
