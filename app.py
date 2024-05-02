from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, Float
# from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import os


from _datetime import datetime

app = Flask(__name__)

Bootstrap5(app)


# CREATE DB
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books.db"
# Create the extension
db = SQLAlchemy(model_class=Base)
# initialise the app with the extension
db.init_app(app)


# CREATE TABLE
class Genre(db.Model):
    __tablename__ = "genre"

    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Genre %r>' % self.id


# CREATE TABLE
class Books(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String(250), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.now())
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id", ondelete="CASCADE"),primary_key=True)
    genre = db.relationship("Genre",  backref="books")

    def __repr__(self):
        return '<Books %r>' % self.id

# Create table schema in the database. Requires application context.
with app.app_context():
    db.create_all()
# exit()


@app.route("/")
def home():
    with app.app_context():
        genres = Genre.query.all()
        books = Books.query.all()
    return render_template("index.html",  books=books, genres=genres)



@app.route('/create')
def create():
    with app.app_context():
        genres = Genre.query.all()
    return render_template("create.html", genres=genres)



@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":

        # save image

        file = request.files['image']
        file.filename = file.filename.replace(" ", "_")
        file.save(f'static/images_update/{file.filename}')



        # CREATE RECORs
        new_book = Books(
            id=request.form.get("id"),
            title=request.form.get("title"),
            author=request.form.get("author"),
            genre_id=request.form.get("genre_id"),
            description=request.form.get("description"),
            rating=request.form.get("rating"),
            image=file.filename,

        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    # return render_template("create.html")



if __name__ == "__main__":
    app.run(debug=True)
