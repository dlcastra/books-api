import requests


API_URL = "http://127.0.0.1:8000"


def test_get_books_api():
    request = requests.get(API_URL + "/books/")
    request_with_pk = requests.get(API_URL + "/books/1")

    if request:
        request.raise_for_status()
        assert request.status_code == 200
    if request_with_pk:
        request_with_pk.raise_for_status()
        assert request_with_pk.status_code == 200


def test_book_not_found():
    request = requests.get(API_URL + "/books/6")

    assert request.status_code == 404
    assert request.json()["message"] == "Book not found"


def test_book_post():
    request = requests.post(
        API_URL + "/books/",
        json={
            "name": "Book",
            "author": 1,
            "genre": "fantasy",
            "date_release": "2022-01-01",
        },
    )

    assert request.status_code == 200


def test_book_post_error():
    request = requests.post(API_URL + "/books/", json={})

    assert request.status_code == 400
    assert request.json()["message"] == "All fields are required"


def test_boob_put():
    request = requests.post(
        API_URL + "/books/1",
        json={
            "name": "Book",
            "author": 1,
            "genre": "fantasy",
            "date_release": "2022-01-01",
        },
    )

    assert request.status_code == 200


def test_book_put_error():
    request = requests.put(
        API_URL + "/books/6",
        json={
            "name": "Book",
            "author": 1,
            "genre": "fantasy",
            "date_release": "2022-01-01",
        },
    )

    assert request.status_code == 404
