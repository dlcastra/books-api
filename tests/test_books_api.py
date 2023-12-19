import json
from datetime import datetime

import pytest
from django.test import Client
from django.urls import reverse

from books.models import Author, Book


@pytest.fixture
def sample_author():
    return Author.objects.create(name="John", surname="Doe", birth_date="1990-01-01")


@pytest.mark.django_db
def test_api_books_get(client: Client):
    author1 = Author.objects.create(name="John", surname="Doe", birth_date="1990-01-01")
    author2 = Author.objects.create(name="Jane", surname="Does", birth_date="1995-05-05")
    book1 = Book.objects.create(name="Book1", author=author1, genre="fantasy", date_release="1990-01-01")
    book2 = Book.objects.create(name="Book2", author=author2, genre="fantasy", date_release="1990-02-02")

    response = client.get(reverse("books_api"))
    response_with_pk = client.get(reverse("books_api", kwargs={"book_pk": book1.id}))

    # Check status code
    assert response.status_code == 200
    assert response_with_pk.status_code == 200

    # Check data
    assert response_with_pk.json()["id"] == book1.id and response_with_pk.json()["id"] != book2.id
    assert response_with_pk.json()["name"] == book1.name
    assert response_with_pk.json()["author"] == {
        "id": book1.author.id,
        "name": book1.author.name,
        "surname": book1.author.surname,
    }
    assert response_with_pk.json()["genre"] == book1.genre
    assert response_with_pk.json()["date_release"] == book1.date_release


@pytest.mark.django_db
def test_api_books_post(client: Client, sample_author):
    data = {
        "name": "Book1",
        "author": sample_author.id,
        "genre": "fantasy",
        "date_release": "2023-06-30",
    }

    response = client.post(reverse("books_api"), data=json.dumps(data), content_type="application/json")

    # Check status code
    assert response.status_code == 200

    # Object creation check
    created_book = Book.objects.get(id=response.json()["id"])
    assert created_book.name == data["name"]
    assert created_book.author.id == sample_author.id
    assert created_book.genre == data["genre"]
    assert str(created_book.date_release) == data["date_release"]

    # Check data
    assert response.json()["name"] == data["name"]
    assert response.json()["author"]["id"] == sample_author.id
    assert response.json()["genre"] == data["genre"]
    assert response.json()["date_release"] == data["date_release"]


@pytest.mark.django_db
def test_api_books_update(client: Client, sample_author):
    book = Book.objects.create(
        name="Book1",
        author=sample_author,
        genre="fantasy",
        date_release="2023-06-30",
    )

    put_data = {
        "name": "TestUpdate",
        "author": sample_author.id,
        "genre": "fiction",
        "date_release": "2023-08-12",
    }

    url = reverse("books_api", kwargs={"book_pk": book.id})
    response = client.put(url, data=json.dumps(put_data), content_type="application/json")

    # Check status code
    assert response.status_code == 200
    assert response.status_code != 404

    # Check data
    date_format = "%Y-%m-%d"
    expected_date_release = datetime.strptime(put_data["date_release"], date_format).date()
    updated_book = Book.objects.get(id=book.id)
    assert updated_book.name == put_data["name"]
    assert updated_book.author == sample_author
    assert updated_book.genre == put_data["genre"]
    assert updated_book.date_release == expected_date_release


@pytest.mark.django_db
def test_api_books_delete(client: Client, sample_author):
    book_for_deleted = Book.objects.create(
        name="ForDeleted",
        author=sample_author,
        genre="fantasy",
        date_release="2023-08-12",
    )

    url = reverse("books_api", kwargs={"book_pk": book_for_deleted.id})
    response = client.delete(url)

    assert response.status_code == 204
    assert response.status_code != 404
    assert response.status_code != 405
