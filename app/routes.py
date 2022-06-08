from app import app
from flask import render_template

@app.route('/')
def index():
    return render_template("index.html.jinja")

@app.route("/author")
def author():
    return render_template("author.html.jinja")

@app.route("/extract")
def extract():
    return render_template("extract.html.jinja")
