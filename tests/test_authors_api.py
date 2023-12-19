import pytest
from django.urls import reverse

from books.models import Author
from django.test import Client


@pytest.mark.django_db
def test_authors_api_get(client: Client):
    author1 = Author.objects.create(name="John", surname="Doe", birth_date="1990-01-01")
    author2 = Author.objects.create(name="Jane", surname="Doe", birth_date="1995-05-05")

    response = client.get(reverse("authors_api"))
    response_with_pk = client.get(
        reverse("authors_api", kwargs={"authors_pk": author1.id})
    )
    response_post = client.post(reverse("authors_api"))
    response_delete = client.delete(reverse("authors_api"))

    # Status code
    assert response.status_code == 200
    assert response_with_pk.status_code == 200
    assert response_post.status_code == 405
    assert response_delete.status_code == 405

    # Data
    assert (
        response_with_pk.json()["id"] == author1.id
        and response_with_pk.json()["id"] != author2.id
    )
    assert response_with_pk.json()["name"] == author1.name
    assert response_with_pk.json()["surname"] == author1.surname
    assert response_with_pk.json()["birth_date"] == author1.birth_date
