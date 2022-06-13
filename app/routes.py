from app import app
from flask import render_template, request, redirect
from urllib import response
from scraper import Movie
from analyzer import save_chart

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
        movie_id=movie.download_information(movie_url)
        save_chart(movie_id)
        return redirect(f"/information/{movie_id}")
    else:
        return render_template("extract.html.jinja")

@app.route("/information/<int:movie_id>")
def information(movie_id):
    movie = Movie()
    movie_data = movie.get_information(movie_id)

    return render_template("information.html.jinja", movie_id=movie_id, filmweb_data=movie_data["filmweb_data"], opinions=movie_data["opinions"], chart=f"/plots/{movie_id}_stars.png")