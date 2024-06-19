from django.urls import path
from .views import login_view
from django.contrib.auth.views import LogoutView

app_name = 'user-login'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
