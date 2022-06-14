from re import T
from flask import render_template, request, redirect, Flask
from urllib import response
from scraper import Movie
from analyzer import save_chart

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///filmweb.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class Filmweb(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    id_url = db.Column(db.String(200), nullable=False)
    title_polish = db.Column(db.String(200), nullable=False)
    kind = db.Column(db.String(200), nullable=False)
    original_title = db.Column(db.String(200), nullable=False)
    release_date = db.Column(db.String(200), nullable=False)
    seasons = db.Column(db.String(200), nullable=False)
    genres = db.Column(db.String(200), nullable=False)
    decription = db.Column(db.String(200), nullable=False)
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
        movie_dict = movie.download_information(movie_url)

        id_url = movie_dict["id_url"]
        title_polish = movie_dict["title_polish"]
        kind = movie_dict["kind"]
        original_title = movie_dict["original_title"]
        release_date = movie_dict["release_date"]
        seasons = movie_dict["seasons"]
        genres = movie_dict["genres"]
        decription = movie_dict["description"]
        number_of_public_rating = movie_dict["number_of_public_rating"]
        critics = movie_dict["critics"]
        director = movie_dict["director"]
        creators = movie_dict["creators"]
        scriptwriter = movie_dict["scriptwriter"]
        actorsArray = movie_dict["actorsArray"]
        allOpinions = movie_dict["allOpinions"]

        current_movie = Filmweb(id_url=id_url, title_polish=title_polish, kind=kind, original_title=original_title, release_date=release_date, 
        seasons=seasons, genres=genres, decription=decription, number_of_public_rating=number_of_public_rating, critics=critics, director=director, 
        creators=creators, scriptwriter=scriptwriter, actorsArray=actorsArray, allOpinions=allOpinions)

        db.session.add(current_movie)
        db.session.commit()

        save_chart(allOpinions, id_url)
        return redirect(f"/information/{id_url}")
    else:
        return render_template("extract.html.jinja")

@app.route("/information/<int:id_url>")
def information(id_url):
    all_movies = Filmweb.query.all()
    for movie in all_movies:
        if movie.id_url == str(id_url):    
            return render_template("information.html.jinja", title = movie.title_polish, image_url = f'/plots/{id_url}_stars.png')

    return render_template("index.html.jinja") 