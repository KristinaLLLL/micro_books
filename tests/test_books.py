import requests

api_url = 'http://localhost:8000'

def test_healthcheck():
    response = requests.get(f'{api_url}/')
    assert response.status_code == 200

class BookServiceTesting():
    def test_get_books(self):
        response = requests.get(f'{api_url}/v1/books')
        assert response.status_code == 200
        assert len(response.json()) == 0

    def test_add_book(self):
        insert = {"title": "Name book", "body": "Book text"}
        response = requests.post(f'{api_url}/v1/books', json=insert)
        assert response.status_code == 200
        assert response.json().get('id') == 4
        assert response.json().get('title') == 'Name book'
        assert response.json().get('body') == 'Book text'

    def test_get_book_by_id(self):
        response = requests.get(f'{api_url}/v1/books/3')
        assert response.status_code == 200
        assert response.json().get('id') == 3
        assert response.json().get('title') == 'Name book'
        assert response.json().get('body') == 'Book text'