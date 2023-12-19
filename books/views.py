import json

from django.http import JsonResponse

from books.models import Author, Book


def authors_api(request, authors_pk=None):
    if request.method == "GET":
        if authors_pk is None:
            authors = Author.objects.all()
            return JsonResponse(
                [
                    {
                        "id": a.id,
                        "name": a.name,
                        "surname": a.surname,
                        "birth_date": a.birth_date,
                    }
                    for a in authors
                ],
                safe=False,
                status=200,
            )
        else:
            author = Author.objects.get(id=authors_pk)
            return JsonResponse(
                {
                    "id": author.id,
                    "name": author.name,
                    "surname": author.surname,
                    "birth_date": author.birth_date,
                }
            )
    else:
        return JsonResponse({"message": "Incorrect method"}, status=405)


def books_api(request, book_pk=None):
    if request.method == "GET":
        if book_pk is None:
            books = Book.objects.all()
            return JsonResponse(
                [
                    {
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
                    for book in books
                ],
                safe=False,
                status=200,
            )
        else:
            try:
                book = Book.objects.get(id=book_pk)
                return JsonResponse(
                    {
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
                )
            except Book.DoesNotExist:
                return JsonResponse({"message": "Book not found"}, status=404)

    elif request.method == "POST":
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

        book = Book.objects.create(name=name, author=author, genre=genre, date_release=date_release)
        return JsonResponse(
            {
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
        )

    elif request.method == "PUT":
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

        return JsonResponse(
            {
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
        )

    elif request.method == "DELETE":
        try:
            book = Book.objects.get(id=book_pk)
        except Book.DoesNotExist:
            return JsonResponse({"message": "Book not found"}, status=404)

        if book:
            book.delete()
            return JsonResponse({"message": "The book was successfully deleted"}, status=204)
        else:
            return JsonResponse({"message": "Error deleting the book"}, status=500)

    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)
