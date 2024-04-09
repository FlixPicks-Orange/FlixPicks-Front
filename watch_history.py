import requests, os

class Movie:
    def __init__(self, id, title, picture):
        self.id = id
        self.title = title
        self.picture = picture

def get_watched_movies(user_id):
    movie_ids = []
    r =requests.get(os.getenv('DB_URL')+"/watch_history/"+ str(user_id))
    print(r.status_code)
    if(r.status_code == 200):
        i=0
        for entry in r.json():
            movie_id = entry['movie_id']
            movie_ids.append(movie_id)
        movie_ids = set(movie_ids)
        liked_ids, disliked_ids = get_rated_movies(user_id)
        movie_ids = movie_ids - set(liked_ids)
        movie_ids = movie_ids - set(disliked_ids)
        return create_movies(movie_ids)

def get_rated_movies(user_id):
    r =requests.get(os.getenv('DB_URL')+"/user_ratings/"+ str(user_id))
    if(r.status_code == 200):
        package = r.json()
        liked_ids = []
        disliked_ids = []
        for entry in package:
            movie_id = entry['movie_id']
            if entry['user_liked'] == True:
                liked_ids.append(movie_id)
            else:
                disliked_ids.append(movie_id)
        return liked_ids, disliked_ids

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