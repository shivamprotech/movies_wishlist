from flask import session
import pytest
from flask import template_rendered
from movies_wishlist import create_app
from mongoengine import connect

from movies_wishlist.main.models import Movie


@pytest.fixture(scope="session")
def app():
    app = create_app("movies_wishlist.config.TestConfig")
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app, client):
    db = connect('test')
    yield db
    db.drop_database('test')

@pytest.fixture
def movie(app, client, db):
    movie = Movie(**{"Title":"Fast & Furious 6","Year":"2013","imdbID":"tt1905041"})
    movie.save()
    yield movie

@pytest.fixture
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)