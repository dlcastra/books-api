import requests

API_URL = "http://127.0.0.1:8000"


def test_api_authors():
    request = requests.get(API_URL + "/authors/")
    request_with_pk = requests.get(API_URL + "/authors/1")

    if request:
        request.raise_for_status()
        assert request.status_code == 200
    if request_with_pk:
        request_with_pk.raise_for_status()
        assert request_with_pk.status_code == 200


def test_author_not_found():
    # There are only 10 authors in the local database at this time
    request = requests.get(API_URL + "/authors/11")

    assert request.status_code == 404


def test_request_method():
    requests_get = requests.get(API_URL + "/authors/1")
    requests_post = requests.post(API_URL + "/authors/")
    requests_put = requests.put(API_URL + "/authors/1")
    requests_delete = requests.delete(API_URL + "/authors/1")

    assert requests_get.status_code == 200
    assert requests_post.status_code == 405
    assert requests_put.status_code == 405
    assert requests_delete.status_code == 405
