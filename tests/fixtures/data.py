from datetime import datetime

import pytest


@pytest.fixture
def meme_cats(freezer, mixer):
    freezer.move_to('2010-10-10')
    return mixer.blend(
        'app.models.memes.Memes',
        title='Мем о котах',
        file_name='images/cats.jpg',
        create_date=datetime.now(),
    )


@pytest.fixture
def meme_dogs(freezer, mixer):
    freezer.move_to('2010-10-10')
    return mixer.blend(
        'app.models.memes.Memes',
        title='Мем о собаках',
        file_name='images/dogs.jpg',
        create_date=datetime.now(),
    )


@pytest.fixture
def meme_monkey(freezer, mixer):
    freezer.move_to('2010-10-10')
    return mixer.blend(
        'app.models.memes.Memes',
        title='Мем об обезьянах',
        file_name='monkey.jpg',
        create_date=datetime.now(),
    )
