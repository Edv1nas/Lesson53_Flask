from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, InputRequired
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField

# from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField

import os
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config["SECRET_KEY"] = "dfgsfdgsdfgsdfgsdf"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "data.sqlite?check_same_thread=False"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


association_table = db.Table(
    "association",
    db.metadata,
    db.Column("father_id", db.Integer, db.ForeignKey("father.id")),
    db.Column("child_id", db.Integer, db.ForeignKey("child.id")),
)


class Father(db.Model):
    __tablename__ = "father"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column("Name", db.String)
    surname = db.Column("Surname", db.String)
    children = db.relationship(
        "Child", secondary=association_table, back_populates="fathers"
    )


class Child(db.Model):
    __tablename__ = "child"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column("Name", db.String)
    surname = db.Column("Surname", db.String)
    fathers = db.relationship(
        "Father", secondary=association_table, back_populates="children"
    )


def get_pk(obj):
    return str(obj)


def child_query():
    return Child.query


def father_query():
    return Father.query


class FatherForm(FlaskForm):
    name = StringField("Name", [DataRequired()])
    surname = StringField("Surname", [DataRequired()])
    children = QuerySelectMultipleField(
        query_factory=child_query,
        get_label="name",
        get_pk=get_pk
    )
    submit = SubmitField("Submit")


class ChildForm(FlaskForm):
    name = StringField("Name", [DataRequired()])
    surname = StringField("Surname", [DataRequired()])
    fathers = QuerySelectMultipleField(
        query_factory=father_query, get_label="name", get_pk=get_pk
    )
    submit = SubmitField("Submit")


@app.route("/parentx", methods=["GET", "POST"])
def get_all_parentx():
    fathers = Father.query.all()
    return render_template("parentx.html", fathers=fathers)


@app.route("/childrenx", methods=["GET", "POST"])
def get_all_childrenx():
    children = Child.query.all()
    return render_template("childrenx.html", children=children)


@app.route("/new_father", methods=["GET", "POST"])
def new_parent():
    db.create_all()
    form = FatherForm()
    if form.validate_on_submit():
        new_father = Father(name=form.name.data, surname=form.surname.data)
        for child in form.children.data:
            assigned_child = Child.query.get(child.id)
            new_father.children.append(assigned_child)
        db.session.add(new_father)
        db.session.commit()
        return redirect(url_for("get_all_parentx"))
    return render_template("new_father.html", form=form)


@app.route("/new_child", methods=["GET", "POST"])
def new_children():
    db.create_all()
    form = ChildForm()
    if form.validate_on_submit():
        new_child = Child(name=form.name.data, surname=form.surname.data)
        for father in form.fathers.data:
            assigned_father = Father.query.get(father.id)
            new_child.fathers.append(assigned_father)
        db.session.add(new_child)
        db.session.commit()
        return redirect(url_for("get_all_childrenx"))
    return render_template("new_child.html", form=form)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
