"""
Forms for reviews.
"""
from django import forms

from .models import Book, Review, Author, Category


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'category', 'image']
        widgets = {
            'author': forms.Select(),
            'category': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].empty_label = '---------'
        self.fields['category'].empty_label = '---------'


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['content', 'rating']


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'description']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
