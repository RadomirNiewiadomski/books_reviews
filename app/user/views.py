"""
Views for the user API.
"""
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.settings import api_settings

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.http import HttpResponse

from user.serializers import UserSerializer, AuthTokenSerializer
from .forms import CustomAuthenticationForm


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return redirect('reviews:index')
        else:
            return HttpResponse('Invalid credentials', status=401)
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})