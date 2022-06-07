from urllib import response
import requests
import json
from bs4 import BeautifulSoup

url = input("Enter link from Filmweb: ")
response = requests.get(url)
id_url = url.split("-")[-1]
page = BeautifulSoup(response.text, "html.parser")

try:
    kind = page.find("div", {"class":"filmCoverSection__type"}).get_text()
except:
    kind = ""

title_polish = page.select_one("h1.filmCoverSection__title").get_text()

try:
    original_title = page.select_one("div.filmCoverSection__originalTitle").get_text() 
except:
    original_title = ""

try:
    release_date = page.select_one("span.block").get_text().strip()
except:
    release_date = None

if release_date == None:
    seasons = page.find("div", {"data-source":"seasonsOrYears"}).get_text()
    seasons = json.loads(seasons)
else:
    seasons = {
        "seasons": [],
    }

try:
    span_genres = page.find("div", {"itemprop":"genre"}).find_all("span")
    genres = []
    for span_genre in span_genres:
        if span_genre.get_text() != " / ":
            genres.append(span_genre.get_text())
except:
    genres = []

try:
    div_genres = page.find("div", {"itemprop":"genre"}).find_all("a")
    genres = []
    for a in div_genres:
        genres.append(a.get_text())
except:
    genres = []

try:
    description = page.select_one("div.filmPosterSection__plot").find("span").get_text()
except:
    try:
        description = page.find("span", {"itemprop":"description"}).get_text().strip()
    except:
        description = ""

public_rating = round(float(page.find("div", {"class":"filmRating filmRating--hasPanel"}).get("datarating-rate")), 2)
number_of_public_rating = int(page.find("div", {"class":"filmRating filmRating--hasPanel"}).get("datarating-count"))

try:
    critics = page.find("div", {"data-source":"criticRatingData"}).get_text()
    critics = json.loads(critics)
except:
    critics = None

try:
    director = page.find("div", {"data-type":"directing-info"}).find("span", {"itemprop":"name"}).get_text()
except:
    director = ""

try:
    div_creators = page.find("div", {"data-type":"creators-info"}).find_all("span", {"itemprop":"name"})
    creators = []
    for div_creator in div_creators:
        creators.append(div_creator.get_text())
except:
    creators = ""

try:
    scriptwriter = page.find("div", {"data-type":"screenwriting-info"}).find("span", {"itemprop":"name"}).get_text()
except:
    scriptwriter = None

pageActorsUrl = f"{url}" + "/cast/actors"
response = requests.get(pageActorsUrl)

pageActors = BeautifulSoup(response.text, "html.parser")

actors = pageActors.find("div", {"class":"filmFullCastSection__list"}).find_all("div", {"class":"castRoleListElement__info"})
actorsArray = []

for index in range(5):
    actorsArray.append(actors[index].get_text())

##### opinie
pageOpinionsUrl = url + "/discussion"

allOpinions = []

while(pageOpinionsUrl):
    response = requests.get(pageOpinionsUrl)
    pageOpinions = BeautifulSoup(response.text, "html.parser")

    opinions = pageOpinions.find_all("li", {"class":"forumSection__item"})

    for opinion in opinions:
        title = opinion.find("a", {"class":"forumSection__itemLink"}).get_text().strip()
        try:
            review = opinion.find("p", {"class":"forumSection__topicText"}).get_text().strip()
            if review == "Uwaga Spoiler! Ten temat może zawierać treści zdradzające fabułę.":
                review = ""
        except:
            review = None

        try:
            author = opinion.find("span", {"class":"forumSection__authorName"}).get_text().strip()
        except:
            author = "użytkownik usunięty"

        try:
            stars = int(opinion.find("span", {"class":"forumSection__starsNo"}).get_text().strip())
        except:
            stars = None

        date = opinion.find("time").get_text()

        try:
            likes = int(opinion.find("span", {"class":"plusMinusWidget__count"}).get_text().strip())
        except:
            likes = None

        try:
            comments = int(opinion.find("span", {"class":"forumSection__commentsCount"}).get_text().strip())
        except:
            likes = None

        allOpinions.append({
            "title": title,
            "review": review,
            "author": author,
            "stars": stars,
            "date": date,
            "likes": likes,
            "comments": comments,
        })
    try:
        pageOpinionsUrl = "https://www.filmweb.pl" + pageOpinions.find("a",{"title" : "następna"}).get("href")
    except:
        pageOpinionsUrl = None

filmweb_data = {
    "title_polish": title_polish,
    "kind": kind,
    "original_title": original_title,
    "release_date": release_date,
    "seasons": seasons["seasons"],
    "genres": genres,
    "description": description,
    "public_rating": public_rating,
    "number_of_public_rating": number_of_public_rating,
    "critics": critics,
    "director": director,
    "creators": creators,
    "scriptwriter": scriptwriter,
    "actorsArray": actorsArray,
}

with open(f"opinions/{id_url}.json", "w", encoding ="UTF-8") as jf:
    json.dump(allOpinions, jf, indent=4, ensure_ascii=False)

with open(f"information/{id_url}_info.json", "w", encoding ="UTF-8") as jf:
    json.dump(filmweb_data, jf, indent=4, ensure_ascii=False)