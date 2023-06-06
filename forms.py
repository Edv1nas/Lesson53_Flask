from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField
import app


def child_query():
    return app.Child.query


def father_query():
    return app.Father.query


class FatherForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    surname = StringField('Surname', [DataRequired()])
    child = QuerySelectField(query_factory=child_query, allow_blank=True,
                             get_label="name", get_pk=lambda obj: str(obj))
    submit = SubmitField('Insert')


class ChildForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    surname = StringField('Surname', [DataRequired()])
    submit = SubmitField('Insert')
