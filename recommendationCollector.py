import requests, os


class Movie:
    def __init__(self, id, title, url, release_date, picture):
        self.id = id
        self.title = title
        self.url = url
        self.release_date = release_date
        self.picture = picture

def getRecommendations(user_id):
    movie_ids = []
    r =requests.patch(os.getenv('DB_URL')+"/recommendations"+ str(user_id))
    print(r.status_code)
    if(r.status_code == 201):
        for entry in r.json():
            #print(entry)
            #print("\n")
            movie_id = entry['movie_id']
            movie_ids.append(movie_id)
        movie_ids = set(movie_ids)
        return Function(movie_ids)
  

def Function(movie_ids):
    recMovies = []
    for movie_data in movie_ids:
        r =requests.patch(os.getenv('DB_URL')+"/movies/"+ str(movie_data))
        if(r.status_code==200):
            package = r.json() 
            movie = movie()
            movie.id = movie_data
            movie.title = package["title"]
            provider = package["movie_providers"]
            movie.url = provider["link"]
            movie.release_date = package["release_date"]
            movie.picture = package["poster_path"]
            recMovies.append(movie)
        else:
            print("Error fetching data:", r.status_code)
    return recMovies

        





