import requests, os

class Movie:
    def __init__(self, id, title, url, release_date, picture, summary):
        self.id = id
        self.title = title
        self.url = url
        self.release_date = release_date
        self.picture = picture
        self.summary = summary


def getmovie(movie_id):
    r =requests.get(os.getenv('DB_URL')+"/movies/"+ str(movie_id))
    if(r.status_code==200):
        entry = r.json()
        package = entry[0]
        title = str(package["title"])
        providers = package["moive_providers"]
        for provider_info in providers:
            url = str(provider_info["link"])
        release_date = str(package["release_date"])
        picture = package["poster_path"]
        summary = package["summary"]
        movie = Movie(movie_id,title,url,release_date,picture,summary)
        return movie