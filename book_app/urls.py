from django.urls import path
from .views import (book_list_view, book_detail_view,
                    book_create_view, book_update_view, book_delete_view, my_book_list_view)
urlpatterns = [
    path('', book_list_view, name='book_list'),
    path('my_books/', my_book_list_view, name='my_book_list'),
    path('create/', book_create_view, name='book_create'),
    path('<int:pk>/', book_detail_view, name='book_detail'),
    path('<int:pk>/update/', book_update_view, name='book_update'),
    path('<int:pk>/delete/', book_delete_view, name='book_delete'),

]