from django.urls import path

from books.views import AuthorsApiView, BooksApiView

urlpatterns = [
    path("authors/", AuthorsApiView.as_view(), name="authors_api"),
    path("authors/<int:authors_pk>", AuthorsApiView.as_view(), name="authors_api"),
    path("books/", BooksApiView.as_view(), name="books_api"),
    path("books/<int:book_pk>", BooksApiView.as_view(), name="books_api"),
]
