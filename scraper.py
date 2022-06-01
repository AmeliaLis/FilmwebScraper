from urllib import response
import requests
import json
from bs4 import BeautifulSoup

url = "https://www.filmweb.pl/film/Doktor+Strange+w+multiwersum+obłędu-2022-836440"
response = requests.get(url)

page = BeautifulSoup(response.text, "html.parser")

kind = page.select_one("div.filmCoverSection__type").get_text()
title_polish = page.select_one("h1.filmCoverSection__title").get_text()
#original_titile = page.select_one("div.filmCoverSection__originalTitle").get_text() #zastanowię sie nad tym, bo nie wszystkie filmy poskie mają angieslki tytuł
release_date = page.select_one("span.block").get_text().strip()
span_genres = page.find("div", {"itemprop":"genre"}).find_all("span")

genres = []
for span_genre in span_genres:
    if span_genre.get_text() != " / ":
        genres.append(span_genre.get_text())

description = page.select_one("div.filmPosterSection__plot").find("span").get_text()
public_rating = page.select_one("span.filmRating__rateValue").get_text()
number_of_public_rating = page.select_one("span.filmRating__count").get_text().strip()

places = page.select_one("div.filmPosterSection__info.filmInfo > div:nth-child(11)").find_all("span")
places_where = []
for place in places:
    if place.get_text() != " / ":
        places_where.append(place.get_text())

director = page.find("div", {"data-type":"directing-info"}).find("span", {"itemprop":"name"}).get_text()
scriptwriter = page.find("div", {"data-type":"screenwriting-info"}).find("span", {"itemprop":"name"}).get_text()

##### aktorzy

pageActorsUrl = f"{url}" + "/cast/actors"
response = requests.get(pageActorsUrl)

pageActors = BeautifulSoup(response.text, "html.parser")

actors = pageActors.find("div", {"class":"filmFullCastSection__list"}).find_all("div", {"class":"castRoleListElement__info"})
actorsArray = []

for index in range(5):
    actorsArray.append(actors[index].get_text())

##### opinie
pageOpinionsUrl = f"{url}" + "/discussion"
while(pageOpinionsUrl):
    response = requests.get(pageOpinionsUrl)
    pageOpinions = BeautifulSoup(response.text, "html.parser")

    opinions = pageOpinions.find_all("li", {"class":"forumSection__item filmCategory"})

    for opinion in opinions:
        review = opinion.find("p", {"class":"forumSection__topicText"}).get_text()
        print(review)
    
    try:
        pageOpinionsUrl = pageOpinions.select_one("a.pagination__link").get("href")
        print(pageOpinionsUrl)
    except TypeError:
        pageOpinionsUrl = None


