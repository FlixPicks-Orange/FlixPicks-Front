import requests, os


class Movie:
    def __init__(self, id, title, picture):
        self.id = id
        self.title = title
        self.picture = picture
        

def getRecommendations(user_id):
    movie_ids = []
    r =requests.get(os.getenv('DB_URL')+"/recommendations/"+ str(user_id))
    print(r.status_code)
    if(r.status_code == 201):
        for entry in r.json():
            movie_id = entry['movie_id']
            movie_ids.append(movie_id)
        movie_ids = set(movie_ids)
        movie_ids = movie_ids - set(filter_watch_history(user_id))
        return Function(movie_ids)
  

def Function(movie_ids):
    recMovies = []
    for movie_data in movie_ids:
        r =requests.get(os.getenv('DB_URL')+"/movies/"+ str(movie_data))
        if(r.status_code==200):
            entry = r.json()
            package = entry[0]
            package["movie_id"] 
            title = str(package["title"])
            picture = package["poster_path"]
            movie = Movie(movie_data,title,picture)
            recMovies.append(movie)
        else:
            print("Error fetching data:", r.status_code)
    return recMovies

        

def filter_watch_history(user_id):
    r = requests.get(os.getenv('DB_URL') + "/watch_history/" + str(user_id))
    if r.status_code == 200:
        watch_history_ids = []
        package = r.json()
        for entry in package:
            if entry['from_recommended'] is True:
                watch_history_ids.append(entry['movie_id'])
    else:
        print("Error fetching data", r.status_code)            

    return set(watch_history_ids)



    

