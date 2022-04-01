from mongoengine import (
    Document,
    StringField,
    ListField,
)
from flask_login import UserMixin
from movies_wishlist.extensions import login_manager
from bson.objectid import ObjectId


@login_manager.user_loader
def load_user(_id):
    return User.objects(_id=ObjectId(_id)).first()


class User(UserMixin, Document):
    _id = StringField()
    username = StringField(required=True)
    password = StringField()
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    fav_movies = ListField(StringField())
