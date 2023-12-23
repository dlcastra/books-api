import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page

from books.models import Author, Book


class AuthorsApiView(View):
    @staticmethod
    def get_authors_api_json(author):
        return {
            "id": author.id,
            "name": author.name,
            "surname": author.surname,
            "birth_date": author.birth_date,
        }

    @method_decorator(cache_page(30 * 15))
    def get(self, request, authors_pk=None):
        if authors_pk is None:
            authors = Author.objects.all()
            json_data = [self.get_authors_api_json(author) for author in authors]
            return JsonResponse(json_data, safe=False, status=200)
        else:
            try:
                author = Author.objects.get(id=authors_pk)
                return JsonResponse(self.get_authors_api_json(author))
            except Author.DoesNotExist:
                return JsonResponse({"message": "Author not found"}, status=404)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return JsonResponse({"message": "Incorrect method"}, status=405)


class BooksApiView(View):
    @staticmethod
    def get_books_api_json(book):
        return {
            "id": book.id,
            "name": book.name,
            "author": {
                "id": book.author.id,
                "name": book.author.name,
                "surname": book.author.surname,
            },
            "genre": book.genre,
            "date_release": book.date_release,
        }

    @method_decorator(cache_page(30 * 15))
    def get(self, request, book_pk=None):
        if book_pk is None:
            books = Book.objects.all()
            json_data = [self.get_books_api_json(book) for book in books]
            return JsonResponse(json_data, safe=False, status=200)
        else:
            try:
                book = Book.objects.get(id=book_pk)
                return JsonResponse(self.get_books_api_json(book))
            except Book.DoesNotExist:
                return JsonResponse({"message": "Book not found"}, status=404)

    def post(self, request):
        try:
            data = json.loads(request.body)
            name = data.get("name")
            author_id = data.get("author")
            genre = data.get("genre")
            date_release = data.get("date_release")
        except json.JSONDecodeError:
            return JsonResponse({"message": "Request body must be JSON"}, status=400)

        if not name or not author_id or not genre or not date_release:
            return JsonResponse({"message": "All fields are required"}, status=400)

        try:
            author = Author.objects.get(id=author_id)
        except Author.DoesNotExist:
            return JsonResponse({"message": "Author not found"}, status=404)
        book = Book.objects.create(
            name=name, author=author, genre=genre, date_release=date_release
        )
        return JsonResponse(self.get_books_api_json(book))

    def put(self, request, book_pk):
        try:
            book = Book.objects.get(id=book_pk)
        except Book.DoesNotExist:
            return JsonResponse({"message": "Book not found"}, status=404)

        try:
            data = json.loads(request.body)
            name = data.get("name")
            author_id = data.get("author")
            genre = data.get("genre")
            date_release = data.get("date_release")
        except json.JSONDecodeError:
            return JsonResponse({"message": "Request body must be JSON"}, status=400)

        if name:
            book.name = name
        if author_id:
            try:
                author = Author.objects.get(id=author_id)
                book.author = author
            except Author.DoesNotExist:
                return JsonResponse({"message": "Author not found"}, status=404)
        if genre:
            book.genre = genre
        if date_release:
            book.date_release = date_release
        book.save()

        return JsonResponse(self.get_books_api_json(book), safe=False, status=200)

    @staticmethod
    def delete(request, book_pk):
        try:
            book = Book.objects.get(id=book_pk)
        except Book.DoesNotExist:
            return JsonResponse({"message": "Book not found"}, status=404)

        if book:
            book.delete()
            return JsonResponse(
                {"message": "The book was successfully deleted"}, status=204
            )
        else:
            return JsonResponse({"message": "Error deleting the book"}, status=500)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return JsonResponse({"message": "Method not allowed"}, status=405)