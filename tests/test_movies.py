import mock


def test_index_template(app, client, db, captured_templates):
    res = client.get('/')
    assert res.status_code == 200
    template, context = captured_templates[0]
    assert template.name == "index.html"


@mock.patch("movies_wishlist.main.routes.get_movies", mock.MagicMock(return_value=[{"Title": "Fast & Furious 6"}]))
def test_search_template(app, client, db, captured_templates):
    res = client.get('/search', data={"name": "Fast & Furious 6"})
    assert res.status_code == 200
    template, context = captured_templates[0]
    assert template.name == "search.html"

@mock.patch("movies_wishlist.main.routes.get_movies", mock.MagicMock(return_value=[{"Title": "Fast & Furious 6"}]))
def test_search(app, client, db, captured_templates):
    res = client.get('/search', data={"name": "Fast & Furious 6"})
    assert res.status_code == 200


@mock.patch("movies_wishlist.main.routes.get_movie_detail", mock.MagicMock(return_value={"Title": "Fast & Furious 6"}))
def test_detail_template(app, client, db, movie, captured_templates):
    res = client.get('/detail/{{movie.imdbID}}', data={"name": "Fast & Furious 6"})
    assert res.status_code == 200
    template, context = captured_templates[0]
    assert template.name == "detail.html"


@mock.patch("movies_wishlist.main.routes.get_movie_detail", mock.MagicMock(return_value={"Title": "Fast & Furious 6"}))
def test_detail(app, client, movie, captured_templates):
    res = client.get('/detail/{{movie.imdbID}}', data={"name": "Fast & Furious 6"})
    assert res.status_code == 200
