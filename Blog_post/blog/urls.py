from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create_post/', views.create_post, name='create_post'),
    path('view_post/<str:post_id>/', views.view_post, name='view_post'),
    path('add_comment/', views.add_comment, name='add_comment'),
]
