import os
from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

import forms

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

app.config['SECRET_KEY'] = 'dfgsfdgsdfgsdfgsdf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, "data.sqlite")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Father(db.Model):
    __tablename__ = "father"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column("name", db.String)
    surname = db.Column("surname", db.String)
    child_id = db.Column(db.Integer, db.ForeignKey("child.id"))
    child = db.relationship("Child")


class Child(db.Model):
    __tablename__ = "child"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column("name", db.String)
    surname = db.Column("surname", db.String)
    # father_id = db.Column(db.Integer, db.ForeignKey("father.id"))


@app.route("/children", methods=["GET", "POST"])
def get_all_children():
    db.create_all()
    children = Child.query.all()
    parent = Father.query.all()
    return render_template("children.html", children=children, parent=parent)


@app.route("/parent", methods=["GET", "POST"])
def get_all_parents():
    db.create_all()
    parent = Father.query.all()
    return render_template("parent.html", parent=parent)


@app.route("/new_child", methods=["GET", "POST"])
def new_child():
    db.create_all()
    forma = forms.ChildForm()
    if forma.validate_on_submit():
        new_child = Child(name=forma.name.data,
                          surname=forma.surname.data)
        db.session.add(new_child)
        db.session.commit()
        return redirect(url_for("get_all_children"))
    return render_template("add_child.html", form=forma)


@app.route("/new_father", methods=["GET", "POST"])
def new_father():
    db.create_all()
    forma = forms.FatherForm()
    if forma.validate_on_submit():
        new_father = Father(name=forma.name.data,
                            surname=forma.surname.data,
                            child_id=forma.child.data)
        db.session.add(new_father)
        db.session.commit()
        return redirect(url_for("get_all_parents"))
    return render_template("add_father.html", form=forma)


if __name__ == "__main__":
    app.run(debug=True)
    db.create_all()
