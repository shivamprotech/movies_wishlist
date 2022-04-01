from flask import Blueprint, flash, render_template, request, redirect, session, url_for
from flask_login import login_user, current_user, logout_user

from movies_wishlist.main.models import Movie
from .models import User
from movies_wishlist.extensions import bcrypt
from movies_wishlist.user.forms import LoginForm, RegistrationForm

user = Blueprint("user", __name__)


def get_fav_movies(fav_movies_ids):
    """Get user fav movies.

    :param fav_movies: list of fav movies id's.
    :return: list of user fav movies.
    """
    movies = []
    for fav_movie in fav_movies_ids:
        movie = Movie.objects(imdbID=fav_movie).first()
        movies.append(movie)
    return movies


@user.route("/register/", methods=["GET", "POST"])
def register():
    """Register a user

    :return: register page and register a user
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password=hashed_password,
        )
        user.save()
        flash("Your account has been created! You are now able to log in", "success")
        return redirect(url_for("user.login"))
    return render_template("register.html", title="Register", form=form)


@user.route("/login/", methods=["GET", "POST"])
def login():
    """Login a user

    :return: login page and login a user
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            session["_user_id"] = str(user._id)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main.index"))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template("login.html", title="Login", form=form)


@user.route("/add_to_wishlist/", methods=["GET", "POST"])
def add_to_wishlist():
    """Add user movie to wishlist

    :return: index page after adding the movie in the wishlist
    """
    user = User.objects(_id=current_user._id).first()
    if request.form.get("imdbID") not in user.fav_movies:
        user.fav_movies.append(request.form["imdbID"])
        user.save(validate=False)
    flash("Movie successfully Added", "info")
    return redirect(url_for("main.index"))


@user.route("/remove_from_wishlist/", methods=["GET", "POST"])
def remove_from_wishlist():
    """Remove movie from user wishlist

    :return: index page after removing the movie in the wishlist
    """
    user = User.objects(_id=current_user._id).first()
    user.fav_movies.remove(request.form["imdbID"])
    user.save(validate=False)
    flash("Movie successfully Removed", "info")
    return redirect(url_for("main.index"))


@user.route("/wishlist/", methods=["GET", "POST"])
def wishlist():
    """Show wishlist.

    :return: wishlist page.
    """
    user = User.objects(_id=current_user._id).first()
    movies = get_fav_movies(user.fav_movies)
    return render_template("wishlist.html", movies=movies)


@user.route("/logout/")
def logout():
    """Logout a user

    :return: logout a user.
    """
    logout_user()
    return redirect(url_for("main.index"))
