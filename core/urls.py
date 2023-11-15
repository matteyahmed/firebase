from django.urls import path
from django.contrib import admin
from django.urls import path

from core import views

urlpatterns = [
        path('login/', views.LoginView.as_view()),
        path('post/', views.PostBlog.as_view(), name='post'),
        path('postlist/', views.getData.as_view(), name='postlist'),
        # path('postall/', views.GetAllBlogs.as_view(), name='postall'),
]