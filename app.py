from flask import render_template, request, redirect, Flask, Response
from movie import Movie
from analyzer import save_chart
import json
from flask_sqlalchemy import SQLAlchemy
import ast

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///filmweb.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

#Klasa, która tworzy strukturę bazy danych
class Filmweb(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    url =db.Column(db.String(200),  nullable=False)
    id_url = db.Column(db.String(200), nullable=False)
    title_polish = db.Column(db.String(200), nullable=False)
    kind = db.Column(db.String(200), nullable=False)
    original_title = db.Column(db.String(200), nullable=False)
    release_date = db.Column(db.String(200), nullable=False)
    seasons = db.Column(db.String(200), nullable=False)
    genres = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    public_rating = db.Column(db.String(200), nullable=False)
    number_of_public_rating = db.Column(db.String(200), nullable=False)
    critics = db.Column(db.String(200), nullable=False)
    director = db.Column(db.String(200), nullable=False)
    creators = db.Column(db.String(200), nullable=False)
    scriptwriter = db.Column(db.String(200), nullable=False)
    actorsArray = db.Column(db.String(200), nullable=False)
    allOpinions = db.Column(db.String(200), nullable=False)

#Pomocnicza funkcja
def string_to_array(string):
    return string.split(",")

#Route do strony głównej, która przekazuje dodatkowo wszystkie dotychczas przekazane dane na temat filmów lub seriali z bazy danych
@app.route('/')
def index():
    movies = Filmweb.query.all()
    return render_template("index.html.jinja", movies = movies)

@app.route("/author")
def author():
    return render_template("author.html.jinja")

@app.route("/extract", methods=["POST", "GET"])
def extract():
    if request.method == "POST":
        try:
            movie_url = request.form.get("movie_url")
            movie=Movie()
            movie_dict = movie.download_information(movie_url)

            url = movie_dict["url"]
            id_url = movie_dict["id_url"]
            title_polish = movie_dict["title_polish"]
            kind = movie_dict["kind"]
            original_title = movie_dict["original_title"]
            release_date = movie_dict["release_date"]
            seasons = movie_dict["seasons"]
            genres = movie_dict["genres"]
            description = movie_dict["description"]
            public_rating = movie_dict["public_rating"]
            number_of_public_rating = movie_dict["number_of_public_rating"]
            critics = movie_dict["critics"]
            director = movie_dict["director"]
            creators = movie_dict["creators"]
            scriptwriter = movie_dict["scriptwriter"]
            actorsArray = movie_dict["actorsArray"]
            allOpinions = movie_dict["allOpinions"]

            prev_movies = Filmweb.query.all()
            for prev_movie in prev_movies:
                if prev_movie.id_url == str(id_url):
                    return render_template("information.html.jinja", movie=prev_movie, image_url = f'/plots/{id_url}_stars.png')

            current_movie = Filmweb(url=url, id_url=id_url, title_polish=title_polish, kind=kind, original_title=original_title, release_date=release_date, 
            seasons=seasons, genres=genres, description=description, public_rating=public_rating, number_of_public_rating=number_of_public_rating, critics=critics, director=director, 
            creators=creators, scriptwriter=scriptwriter, actorsArray=actorsArray, allOpinions=allOpinions)

            db.session.add(current_movie)
            db.session.commit()

            save_chart(allOpinions, id_url)
            return redirect(f"/information/{id_url}")
        except:
            return render_template("extract.html.jinja", error = "Ups... Coś poszło nie tak")
    else:
        return render_template("extract.html.jinja")

@app.route("/information/<int:id_url>")
def information(id_url):
    all_movies = Filmweb.query.all()
    for movie in all_movies:
        if movie.id_url == str(id_url):
            allOpinions = ast.literal_eval(movie.allOpinions)
            genres = string_to_array(movie.genres)
            critics = ast.literal_eval(movie.critics)
            if movie.kind == "Film":
                information1 = "Data premiery: " + movie.release_date
                information2 = "Reżyser: " + movie.director + "; Autor scenariusza: " + movie.scriptwriter
            else:
                information1 = "Liczba sezonów: " + movie.seasons
                information2 = "Twórcy: " + movie.creators

            return render_template("information.html.jinja", movie=movie, image_url = f'/plots/{id_url}_stars.png', allOpinions = allOpinions, genres = genres, critics=critics, information1 = information1, information2= information2)

    return render_template("index.html.jinja") 

@app.route("/delete/<int:id_url>")
def delete(id_url):
    movies = Filmweb.query.all()
    for movie in movies:
        if movie.id_url == str(id_url):
            filmweb_id = movie.id #id w bazie danych (kolejność filmu)
    movie_to_delete = Filmweb.query.get_or_404(filmweb_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect("/")

@app.route("/get_json/<int:id_url>")
def get_json(id_url):
    movies = Filmweb.query.all()
    for movie in movies:
        if movie.id_url == str(id_url):
            movie_url = movie.url
    movie = Movie()
    data = movie.download_information(movie_url)
    allOpinions = data["allOpinions"]
    allOpinions = ast.literal_eval(allOpinions)
    data["allOpinions"] = allOpinions
    content = json.dumps(data, indent = 4, ensure_ascii=False)
    return Response(content,
        mimetype = "application/json",
        headers = {"Content-Dispositon":f"attachment; filename={id_url}.json"})