from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from reviews.models import Category, Author, Book, Review
import random


class Command(BaseCommand):
    """Command to add initial data to database if there is no data in db (in DEV mode)."""

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Checking for existing initial data...'))

        # Check and create categories
        categories = [
            'Biography', 'Science Fiction', 'Fantasy', 'Mystery', 'Romance', 
            'Thriller', 'Non-Fiction', 'Historical', 'Young Adult', 'Children', 
            'Adventure', 'Horror', 'Self-Help', 'Travel', 'Cooking'
        ]
        for category in categories:
            if not Category.objects.filter(name=category).exists():
                Category.objects.create(name=category)
        self.stdout.write(self.style.SUCCESS('Categories created or already exist.'))

        # Check and create authors
        authors = [
            ('John West', 'An author of many books.'),
            ('Jane Doe', 'An author of science fiction books.'),
            ('Alice Smith', 'An author of fantasy novels.'),
            ('Robert Brown', 'Writes thrilling mysteries.'),
            ('Emily White', 'Known for her romance novels.'),
            ('Michael Green', 'A famous non-fiction author.'),
            ('Laura Black', 'Author of young adult novels.'),
            ('Chris Red', 'Writes historical fiction.'),
            ('Nina Blue', 'Popular for children’s books.'),
            ('Oliver Grey', 'Adventure book writer.')
        ]
        for name, description in authors:
            if not Author.objects.filter(name=name).exists():
                Author.objects.create(name=name, description=description)
        self.stdout.write(self.style.SUCCESS('Authors created or already exist.'))

        # Check and create books
        books = [
            ('Life of John', 'A biography of John West. This book delves deep into his life and accomplishments, highlighting his significant contributions to literature and society.', 'Biography', 'John West'),
            ('The Future', 'A science fiction novel by Jane Doe. Set in a dystopian future, it explores themes of technology and humanity.', 'Science Fiction', 'Jane Doe'),
            ('Magic World', 'A fantasy novel by Alice Smith. It tells the story of a young hero in a land filled with magic and mystery.', 'Fantasy', 'Alice Smith'),
            ('Mystery Mansion', 'A thrilling mystery by Robert Brown. Follow the detective as they uncover secrets hidden in the old mansion.', 'Mystery', 'Robert Brown'),
            ('Love Story', 'A romance novel by Emily White. This heartwarming tale explores the journey of love and relationships.', 'Romance', 'Emily White'),
            ('True Stories', 'A collection of non-fiction stories by Michael Green. These real-life accounts are both inspiring and educational.', 'Non-Fiction', 'Michael Green'),
            ('Teen Tales', 'Young adult stories by Laura Black. These tales capture the essence of teenage life and its challenges.', 'Young Adult', 'Laura Black'),
            ('Historic Times', 'Historical fiction by Chris Red. Set in ancient times, this book brings history to life through engaging narratives.', 'Historical', 'Chris Red'),
            ('Children Adventures', 'Children’s books by Nina Blue. These stories are filled with adventure and valuable life lessons for kids.', 'Children', 'Nina Blue'),
            ('Epic Journeys', 'Adventure stories by Oliver Grey. Embark on epic journeys through unknown lands and face thrilling challenges.', 'Adventure', 'Oliver Grey'),
            ('Scary Nights', 'A horror book by Chris Red. Experience spine-chilling tales that will keep you up at night.', 'Horror', 'Chris Red'),
            ('Mindful Living', 'Self-help book by Laura Black. Learn about mindfulness and living a balanced life through practical advice.', 'Self-Help', 'Laura Black'),
            ('Around the World', 'Travel stories by Michael Green. Discover the wonders of the world through the eyes of the author.', 'Travel', 'Michael Green'),
            ('Gourmet Cooking', 'A cookbook by Emily White. Explore gourmet recipes and culinary techniques from around the globe.', 'Cooking', 'Emily White'),
            ('Fantastic Futures', 'More science fiction by Jane Doe. Dive into futuristic worlds with innovative technology and complex characters.', 'Science Fiction', 'Jane Doe')
        ]
        for title, description, category_name, author_name in books:
            if not Book.objects.filter(title=title).exists():
                author = Author.objects.get(name=author_name)
                category = Category.objects.get(name=category_name)
                Book.objects.create(
                    title=title,
                    description=description,
                    category=category,
                    author=author
                )
        self.stdout.write(self.style.SUCCESS('Books created or already exist.'))

        # Check and create users
        User = get_user_model()
        users = [
            ('user1@example.com', 'password123', 'User One'),
            ('user2@example.com', 'password123', 'User Two'),
            ('user3@example.com', 'password123', 'User Three'),
            ('user4@example.com', 'password123', 'User Four'),
            ('user5@example.com', 'password123', 'User Five')
        ]
        for email, password, name in users:
            if not User.objects.filter(email=email).exists():
                User.objects.create_user(email=email, password=password, name=name)
        self.stdout.write(self.style.SUCCESS('Users created or already exist.'))

        # Check and create reviews
        if not Review.objects.exists():
            self.stdout.write(self.style.SUCCESS('Creating reviews...'))
            all_books = Book.objects.all()
            all_users = User.objects.all()
            review_content = [
                'An inspiring biography.', 'A fascinating sci-fi novel.', 'An enchanting fantasy story.',
                'A thrilling mystery.', 'A beautiful romance.', 'An insightful non-fiction.',
                'An exciting young adult story.', 'A captivating historical fiction.', 'A delightful children’s book.',
                'An epic adventure.', 'A spine-chilling horror.', 'A helpful self-help book.',
                'A fantastic travel story.', 'A delicious cookbook.', 'Another amazing sci-fi novel.'
            ]
            for book in all_books:
                for user in all_users:
                    content = random.choice(review_content)
                    rating = random.randint(1, 5)
                    Review.objects.create(book=book, reviewer=user, content=content, rating=rating)
        else:
            self.stdout.write(self.style.SUCCESS('Reviews already exist.'))

        self.stdout.write(self.style.SUCCESS('Initial data check and creation completed successfully.'))
