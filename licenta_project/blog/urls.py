from django.urls import path
from .views import (PostListView, 
                    PostDetailView, 
                    PostCreateView,
                    PostUpdateView,
                    PostDeleteView,
                    UserPostListView,
                    ClassifierView,
                    ActivityFeedView)
from . import views
from virtual_garden.views import VirtualGardenView

urlpatterns = [
    path('', ClassifierView.as_view(), name='blog-classifier'),
    path('activity/', ActivityFeedView.as_view(), name='activity-feed'),
    path('flowers/', VirtualGardenView.as_view(), name='virtual-garden'),
    path('blog/', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
]