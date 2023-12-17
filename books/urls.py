from django.urls import path

from books import views

urlpatterns = [
    path("authors/", views.authors_api, name="authors_api"),
    path("authors/<int:authors_pk>", views.authors_api, name="authors_api"),
    path("books/", views.books_api, name="books_api"),
    path("books/<int:book_pk>", views.books_api, name="books_api"),
]
