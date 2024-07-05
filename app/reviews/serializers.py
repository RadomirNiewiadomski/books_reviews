"""
Serializers for menu API.
"""
from rest_framework import serializers

from reviews.models import Category, Author, Book, Review


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for category."""
    
    class Meta:
        model = Category
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for author."""
    
    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    """Serializer for book."""

    class Meta():
        model = Book
        fields = ['id',
                  'title',
                  'author',
                  'average_rating',
                  'created_at',
                  'image',
                  ]
        read_only_fields = ['id']


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for review."""

    class Meta:
        model = Review
        fields = ['id',
                  'book',
                  'reviewer',
                  'content',
                  'rating',
                  'created_at'
                  ]
        read_only_fields = ['id']


class BookDetailSerializer(BookSerializer):
    """Serializer for book detail view."""

    class Meta():
        model = Book
        fields = ['id',
                  'title',
                  'author',
                  'description',
                  'average_rating',
                  'created_at',
                  'image',
                  ]
        read_only_fields = ['id']


class BookImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to books."""

    class Meta:
        model = Book
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': 'True'}}
