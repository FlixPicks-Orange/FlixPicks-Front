import requests, os
from datetime import datetime

class Movie:
    def __init__(self, id, title, genres, providers, release_date, picture, summary):
        self.id = id
        self.title = title
        self.genres = genres
        self.providers = providers
        self.release_date = release_date
        self.picture = picture
        self.summary = summary


class Provider:
    def __init__(self, url, logo, name):
        self.url = url
        self.logo = logo
        self.name = name


def getmovie(movie_id):
    r =requests.get(os.getenv('DB_URL')+"/movies/"+ str(movie_id))
    if(r.status_code==200):
        entry = r.json()
        package = entry[0]
        title = str(package["title"])
        services = package["moive_providers"]
        genres = []
        movie_genres = package["movie_genres"]
        for genre in movie_genres:
            genres.append(str(genre["genre_name"]))
        url = []
        logo = []
        name = []
        for provider_info in services:
            url.append(str(provider_info["link"]))
            logo.append(str(provider_info["logo_path"]))
            name.append(str(provider_info["provider_name"]))
        release_date = translate_date(str(package["release_date"]))
        picture = package["poster_path"]
        summary = package["summary"]
        providers = Provider(url, logo, name)
        movie = Movie(movie_id,title, genres,providers,release_date,picture,summary)
        return movie
    
def translate_date(numerical_date):
    # Parse the numerical date string into a datetime object
    date_object = datetime.strptime(numerical_date, "%Y-%m-%d")
    
    # Format the datetime object into the desired string representation
    string_date = date_object.strftime("%B %d, %Y")
    
    # Add the appropriate suffix to the day
    if 4 <= date_object.day <= 20 or 24 <= date_object.day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][date_object.day % 10 - 1]
    
    string_date = string_date.replace(str(date_object.day), str(date_object.day) + suffix)

    return string_date