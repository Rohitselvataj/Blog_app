# blog/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_post, name='add_post'),
    path('my_posts/', views.my_posts, name='my_posts'),
    path('upload_image/', views.upload_image, name='upload_image'),  # Add this line
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
]