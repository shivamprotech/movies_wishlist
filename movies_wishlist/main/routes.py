import requests
from movies_wishlist.constants import URL
from flask import Blueprint, render_template, request
from movies_wishlist.main.forms import SearchForm
from movies_wishlist.main.models import Movie, MovieDetail
from flask import current_app as app

main = Blueprint("main", __name__)


def filter_movies_with_no_images(movie_list):
    """Return movies with contains poster

    :param movie_list: list of movies.
    :return: list of filtered movies.
    """
    return [movie for movie in movie_list if movie.get("Poster") != "N/A"]


def get_movies(name):
    """Get the movies from OMDB API

    :param name: name of the movie.
    :return: list of filtered movies.
    """
    params = {"apikey": app.config.get("API_KEY")}
    params.update({"s": name})
    response = requests.get(URL, params=params)
    for movie in response.json().get("Search"):
        movie["Tag"] = name
    return filter_movies_with_no_images(response.json().get("Search"))


def get_movie_detail(id):
    """Get a single movie from OMDB API

    :param id: IMDB ID
    :return: single movie.
    """
    params = {"apikey": app.config.get("API_KEY")}
    params.update({"i": id})
    response = requests.get(URL, params=params)
    return response.json()


@main.route("/", methods=["POST", "GET"])
def index():
    """Return index.html.

    :return: index page.
    """
    form = SearchForm()
    return render_template("index.html", form=form)


@main.route("/search", methods=["POST", "GET"])
def search():
    """Search for specific movie.

    :return: search page with filtered movies.
    """
    if request.method == "POST":
        movies = Movie.objects(Tag=request.form["name"]).all()
        if len(movies) > 0:
            return render_template("index.html", movies=movies)
    filtered_movies = get_movies(request.form["name"])
    movie_instances = [Movie(**data) for data in filtered_movies]
    Movie.objects.insert(movie_instances, load_bulk=False)
    return render_template("search.html", movies=filtered_movies)


@main.route("/detail/<string:imdbID>", methods=["GET", "POST"])
def detail(imdbID):
    """Returns single movie deatails

    :param imdbID: IMDB ID.
    :return: detail oage with single movie.
    """
    movie = Movie.objects(imdbID=imdbID).first()
    details = MovieDetail.objects(Movie=movie).first()
    if details:
        return render_template("detail.html", movie=details)
    response = get_movie_detail(imdbID)
    details = MovieDetail(
        Movie=movie,
        Rated=response.get("Rated"),
        Released=response.get("Released"),
        Runtime=response.get("Runtime"),
        Genre=response.get("Genre"),
        Director=response.get("Director"),
        Writer=response.get("Writer"),
        Actors=response.get("Actors"),
        Plot=response.get("Plot"),
        Language=response.get("Language"),
        imdbRating=response.get("imdbRating"),
        imdbVotes=response.get("imdbVotes"),
    )
    details.save()
    return render_template("detail.html", movie=details)
