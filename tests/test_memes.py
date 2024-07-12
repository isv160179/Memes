import os

from app.core.constants import DOWNLOAD_DIR


def get_file(file_name: str):
    return {
        'file': (
            file_name, open('tests/fixtures/images/' + file_name, 'rb'),
            'image/jpg')
    }


def add_meme(client, file_name: str, text: str):
    return client.post(
        '/memes/',
        files=get_file(file_name), params={'text': text, }
    )


def test_add_meme(test_client):
    response = add_meme(
        test_client,
        'cats.jpg',
        'meme_about_cats'
    )
    assert response.status_code == 200


def test_get_all_memes(test_client, meme_cats, meme_dogs, meme_monkey):
    PAGE = 1
    SIZE = 2
    response = test_client.get(f'/memes/?page={PAGE}&size={SIZE}')
    assert response.status_code == 200
    assert len(response.json()['items']) == SIZE
    assert response.json() == {
        "items": [
            {
                "title": "Мем о котах",
                "file_name": "images/cats.jpg",
                "id": 1,
                "create_date": "2010-10-10T00:00:00"
            },
            {
                "title": "Мем о собаках",
                "file_name": "images/dogs.jpg",
                "id": 2,
                "create_date": "2010-10-10T00:00:00"
            },
        ],
        "total": 3,
        "page": PAGE,
        "size": SIZE,
        "pages": 2
    }


def test_get_by_id(test_client):
    ID = 2
    add_meme(
        test_client,
        'cats.jpg',
        'meme_about_cats'
    )
    add_meme(
        test_client,
        'dogs.jpg',
        'meme_about_dogs'
    )
    response = test_client.get(f'/memes/{ID}')
    assert response.status_code == 200
    assert len(response.json()) == 4
    keys = sorted(
        [
            'title',
            'file_name',
            'id',
            'create_date',
        ]
    )
    assert (sorted(list(response.json().keys())) == keys)
    assert response.json()['id'] == ID
    file_path = DOWNLOAD_DIR + response.json()['file_name']
    assert os.path.exists(file_path)


def test_put_by_id(test_client):
    add_meme(
        test_client,
        'cats.jpg',
        'meme_about_cats'
    )
    response = test_client.put(
        '/memes/1',
        files=get_file('other_dog.jpg'), params={'text': 'other dog meme', }
    )
    assert response.status_code == 200
    assert response.json()['title'] == 'other dog meme'
    assert 'other_dog' in response.json()['file_name']


def test_delete_meme(test_client):
    add_meme(
        test_client,
        'cats.jpg',
        'meme_about_cats'
    )
    response = test_client.delete('/memes/1')
    assert response.status_code == 200
    response = test_client.get('/memes/1')
    assert response.status_code == 404
