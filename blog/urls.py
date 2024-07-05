from django.urls import path
from .views import index_view, about_view, contact_view, category_view, blog_detail_view, tag_view, search_view

urlpatterns = [
    path('', index_view),
    path('about/', about_view),
    path('contact/', contact_view),
    path('category/<int:pk>/', category_view),
    path('blog/<int:pk>/', blog_detail_view),
    path('tag/', tag_view),
    path('search/', search_view),
]
