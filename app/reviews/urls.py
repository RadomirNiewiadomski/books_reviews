"""
URL mappings for the menu app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import BookViewSet, ReviewViewSet
from .views import BookListView, BookDetailView, AddBookView, add_review

router = DefaultRouter()
router.register('book', BookViewSet)
router.register('review', ReviewViewSet)

app_name = 'reviews'

urlpatterns = [
    path('api/', include((router.urls, 'reviews-api'), namespace='reviews-api')),
    path('', BookListView.as_view(), name='index'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('add_book/', AddBookView.as_view(), name='add_book'),
    path('book/<int:book_id>/add_review/', add_review, name='add_review'),
]
