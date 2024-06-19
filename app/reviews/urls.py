"""
URL mappings for the reviews app.
"""
from django.urls import path
from .views import BookListView, BookDetailView, AddBookView, AddAuthorView, AddCategoryView, add_review

app_name = 'reviews'

urlpatterns = [
    path('', BookListView.as_view(), name='index'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('add_book/', AddBookView.as_view(), name='add_book'),
    path('add_author/', AddAuthorView.as_view(), name='add_author'),
    path('add_category/', AddCategoryView.as_view(), name='add_category'),
    path('book/<int:book_id>/add_review/', add_review, name='add_review'),
]
