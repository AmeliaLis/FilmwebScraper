import requests
import json
from bs4 import BeautifulSoup

class Movie():
    def __init__(self, id=0):
        self.id = id
        self.filmweb_data = []
        self.url = ""
    
    #Pomocnicza funkcja do zamiany tablicy na tekst, przy tworzeniu informacji, które można wykorzystać w bazie danych
    def array_to_string(self, array):
        string = ""
        for item in array:
            string += f"{str(item)}, "
        return string

    #Główna funkcja do zbierania (scrapowania) danych ze strony na temat filmu lub serialu
    def download_information(self,url):
        response = requests.get(url)
        self.url= url
        id_url = int(url.split("-")[-1])
        page = BeautifulSoup(response.text, "html.parser")

        try:
            kind = page.find("div", {"class":"filmCoverSection__type"}).get_text()
        except:
            kind = ""

        try:
            title_polish = page.select_one("h1.filmCoverSection__title").get_text()
        except:
            title_polish = ""

        try:
            original_title = page.select_one("div.filmCoverSection__originalTitle").get_text() 
        except:
            original_title = ""

        try:
            release_date = page.select_one("span.block").get_text().strip()
        except:
            release_date = ""

        try:
            seasons = page.find("div", {"data-source":"seasonsOrYears"}).get_text()
            seasons = len(json.loads(seasons)["seasons"])
        except:
            seasons = 0

        # try:
        #     span_genres = page.find("div", {"itemprop":"genre"}).find_all("span")
        #     genres = []
        #     for span_genre in span_genres:
        #         if span_genre.get_text() != " / ":
        #             genres.append(span_genre.get_text())
        #     genres = self.array_to_string(genres)
        # except:
        #     genres = ""

        try:
            div_genres = page.find("div", {"itemprop":"genre"}).find_all("a")
            genres = []
            for a in div_genres:
                genres.append(a.get_text())
            genres = self.array_to_string(genres)
        except:
            genres = ""

        try:
            description = page.select_one("div.filmPosterSection__plot").find("span").get_text()
        except:
            try:
                description = page.find("span", {"itemprop":"description"}).get_text().strip()
            except:
                description = ""

        public_rating = str(round(float(page.find("div", {"class":"filmRating filmRating--hasPanel"}).get("datarating-rate")), 2))
        number_of_public_rating = str(page.find("div", {"class":"filmRating filmRating--hasPanel"}).get("datarating-count"))

        try:
            critics = page.find("div", {"data-source":"criticRatingData"}).get_text()
            critics = json.loads(critics)
            critics = str(critics)
        except:
            critics = "0"

        try:
            director = page.find("div", {"data-type":"directing-info"}).find("span", {"itemprop":"name"}).get_text()
        except:
            director = ""

        try:
            div_creators = page.find("div", {"data-type":"creators-info"}).find_all("span", {"itemprop":"name"})
            creators = []
            for div_creator in div_creators:
                creators.append(div_creator.get_text())
            creators = self.array_to_string(creators)
        except:
            creators = ""

        try:
            scriptwriter = page.find("div", {"data-type":"screenwriting-info"}).find("span", {"itemprop":"name"}).get_text()
        except:
            scriptwriter = ""

        pageActorsUrl = f"{url}" + "/cast/actors"
        response = requests.get(pageActorsUrl)

        pageActors = BeautifulSoup(response.text, "html.parser")

        actors = pageActors.find("div", {"class":"filmFullCastSection__list"}).find_all("div", {"class":"castRoleListElement__info"})
        actorsArray = []

        for actor in actors:
            actorsArray.append(actor.get_text())
        actorsArray = self.array_to_string(actorsArray)

        #Pobieranie opinii
        pageOpinionsUrl = url + "/discussion"

        allOpinions = []

        while(pageOpinionsUrl):
            response = requests.get(pageOpinionsUrl)
            pageOpinions = BeautifulSoup(response.text, "html.parser")

            opinions = pageOpinions.find_all("li", {"class":"forumSection__item"})

            for opinion in opinions:
                #Link do aktualnej opinii
                opinion_url = "https://www.filmweb.pl" + opinion.find("a", {"class":"forumSection__itemLink"}).get("href").strip()
                title = opinion.find("a", {"class":"forumSection__itemLink"}).get_text().strip()
                try:
                    review = opinion.find("p", {"class":"forumSection__topicText"}).get_text().strip()
                    if review == "Uwaga Spoiler! Ten temat może zawierać treści zdradzające fabułę.":
                        review = "Recenzja zawierała spoilery."
                except:
                    review = ""

                try:
                    author = opinion.find("span", {"class":"forumSection__authorName"}).get_text().strip()
                except:
                    author = "użytkownik usunięty"

                try:
                    stars = opinion.find("span", {"class":"forumSection__starsNo"}).get_text().strip()
                except:
                    stars = "0"

                date = opinion.find("time").get_text()

                try:
                    likes = opinion.find("span", {"class":"plusMinusWidget__count"}).get_text().strip()
                except:
                    likes = "0"

                try:
                    comments = opinion.find("span", {"class":"forumSection__commentsCount"}).get_text().strip()
                except:
                    comments = "0"

                if review != "":
                    allOpinions.append({
                        "opinion_url": opinion_url,
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
                pageOpinionsUrl = ""

        self.filmweb_data = {
            "url":url,
            "id_url": id_url,
            "title_polish": title_polish,
            "kind": kind,
            "original_title": original_title,
            "release_date": release_date,
            "seasons": seasons,
            "genres": genres,
            "description": description,
            "public_rating": public_rating,
            "number_of_public_rating": number_of_public_rating,
            "critics": critics,
            "director": director,
            "creators": creators,
            "scriptwriter": scriptwriter,
            "actorsArray": actorsArray,
            "allOpinions":self.array_to_string(allOpinions)
        }
        return self.filmweb_data