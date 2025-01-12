from django.urls import path
from .views import BlogPostListView, BlogPostDetailsView, SubscribeView

urlpatterns = [
    path('posts/', BlogPostListView.as_view(), name="posts-list"),
    path('posts/<int:pk>/', BlogPostDetailsView.as_view(), name="blogpost-detail"),

    path('subscribe/', SubscribeView.as_view(), name='subscribe'),

]
