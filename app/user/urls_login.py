"""
URL mappings for the user login.
"""

from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import login_view

app_name = 'user-login'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
