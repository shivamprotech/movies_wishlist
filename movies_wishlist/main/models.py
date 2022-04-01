from mongoengine import (
    Document,
    StringField,
    IntField,
    ReferenceField,
)


class Movie(Document):
    Title = StringField(required=True)
    Year = IntField()
    imdbID = StringField()
    Type = StringField()
    Poster = StringField()
    Tag = StringField()


class MovieDetail(Document):
    Movie = ReferenceField(Movie)
    Rated = StringField()
    Released = StringField()
    Runtime = StringField()
    imdbRating = StringField()
    imdbVotes = StringField()
    Genre = StringField()
    Director = StringField()
    Writer = StringField()
    Actors = StringField()
    Plot = StringField()
    Language = StringField()
    meta = {"allow_inheritance": True}
