from app import app
from flask import render_template, request, redirect
from urllib import response
from scraper import Movie
from analyzer import save_chart

from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///filmweb.db"
db = SQLAlchemy(app)

class Filmweb(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    id_url = db.Column(db.String(200), nullable=False)
    title_polish = db.Column(db.String(200), nullable=False)
    kind = db.Column(db.String(200), nullable=False)
    originial_title = db.Column(db.String(200), nullable=False)
    release_date = db.Column(db.String(200), nullable=False)
    seasons = db.Column(db.String(200), nullable=False)
    genres = db.Column(db.String(200), nullable=False)
    desrciption = db.Column(db.String(200), nullable=False)
    number_of_public_rating = db.Column(db.String(200), nullable=False)
    critics = db.Column(db.String(200), nullable=False)
    director = db.Column(db.String(200), nullable=False)
    creators = db.Column(db.String(200), nullable=False)
    scriptwriter = db.Column(db.String(200), nullable=False)
    actorsArray = db.Column(db.String(200), nullable=False)
    allOpinions = db.Column(db.String(200), nullable=False)


@app.route('/')
def index():
    return render_template("index.html.jinja")

@app.route("/author")
def author():
    return render_template("author.html.jinja")

@app.route("/extract", methods=["POST", "GET"])
def extract():
    if request.method == "POST":
        movie_url = request.form.get("movie_url")
        movie=Movie()
        id_url=movie.download_information(movie_url)["id_url"]
        save_chart(id_url)
        return redirect(f"/information/{id_url}")
    else:
        return render_template("extract.html.jinja")

@app.route("/information/<int:id_url>")
def information(id_url):
    movie = Movie()
    movie_data = movie.get_information(id_url)

    return render_template("information.html.jinja", id_url=id_url, filmweb_data=movie_data["filmweb_data"], opinions=movie_data["opinions"], chart=f"/plots/{id_url}_stars.png")