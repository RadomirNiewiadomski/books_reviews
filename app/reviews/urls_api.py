"""
URL mappings for the reviews API.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import BookViewSet, ReviewViewSet

router = DefaultRouter()
router.register('book', BookViewSet)
router.register('review', ReviewViewSet)

app_name = 'reviews-api'

urlpatterns = [
    path('', include(router.urls)),
]
