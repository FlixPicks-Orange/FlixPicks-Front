import requests, os

class Movie:
    def __init__(self, id, title, picture):
        self.id = id
        self.title = title
        self.picture = picture

def get_trending_movies():
    movie_ids = []
    r =requests.get(os.getenv('DB_URL')+"/movies/popular")
    print(r.status_code)
    if(r.status_code == 200):
        for entry in r.json():
            movie_id = entry['movie_id']
            movie_ids.append(movie_id)
        movie_ids = set(movie_ids)
        return create_movies(movie_ids)

def create_movies(movie_ids):
    movies = []
    for movie_data in movie_ids:
        r =requests.get(os.getenv('DB_URL')+"/movies/"+ str(movie_data))
        if(r.status_code==200):
            entry = r.json()
            package = entry[0]
            package["movie_id"] 
            title = str(package["title"])
            picture = package["poster_path"]
            movie = Movie(movie_data,title,picture)
            movies.append(movie)
        else:
            print("Error fetching data:", r.status_code)
    return movies