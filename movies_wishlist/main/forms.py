from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    name = StringField(
        "Search",
        validators=[DataRequired()],
        render_kw={"placeholder": "Search movie/series name..."},
    )
    submit = SubmitField("Search")
