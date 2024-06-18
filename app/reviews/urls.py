"""
URL mappings for the menu app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from reviews import views


router = DefaultRouter()
router.register('book', views.BookViewSet)
router.register('review', views.ReviewViewSet)

app_name = 'reviews'

urlpatterns = [
    path('', include(router.urls)),
]
