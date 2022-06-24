"""Defines URL patterns for users"""

from django.urls import path, include

from . import views

# Set app name so Django can distinguish these user urls from other app urls
app_name = 'users'
urlpatterns = [
    # Include default auth urls, this statement gives prewritten Django user URLs
    # Things like login, logout, etc. will be included with default view functions
    path('', include('django.contrib.auth.urls')),
    # Regristration page.
    path('register/', views.register, name='register'),
]