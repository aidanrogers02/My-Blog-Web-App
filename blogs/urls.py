"""Defines URL patterns for blogs"""

from django.urls import path

from . import views

app_name = 'blogs'
urlpatterns = [
    # Home page
    path('', views.index, name = 'index'),
    # Page that shows all blog posts
    path('posts/', views.posts, name='posts'),
    # Detail page for a single post
    path('posts/<int:post_id>/', views.post, name='post'),
    # Page for adding a new post
    path('new_post/', views.new_post, name='new_post'),
    # Page for adding a new comment
    path('new_comment/<int:post_id>/', views.new_comment, name='new_comment'),
    # Page for editing a post
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    # Page of users the user is following
    path('following/', views.following, name='following'),
    # Home page for user
    path('<str:userpage_id>/', views.user_page, name='user_page'),
    # Page for follow count
    path('followers_count', views.followers_count, name='followers_count'),
]