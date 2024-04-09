import requests, os

'''
def get_survey_subscription():
    subscriptions = [{"Name":"Netflix", "image":"../static/images/netflix.svg"},
            {"Name": "MAX", "image": "../static/images/max.svg"},
            {"Name": "Disney+", "image": "../static/images/disney+.svg"},
            {"Name": "Prime Video", "image": "../static/images/prime_video.svg"},
            {"Name": "Hulu", "image": "../static/images/hulu.svg"},
            ]
    return subscriptions
'''
'''
def get_survey_movies() :
    movies = [{"Name": "Dune", "image": "../static/images/dune_poster.jpg"},
       {"Name": "The Matrix", "image": "../static/images/matrix_poster.jpg"},
       {"Name": "Barbie", "image": "../static/images/barbie_movie_poster.jpg"},
       {"Name": "Friday", "image": "../static/images/friday_poster.jpg"},
    ]
    return movies
    '''
class Movie:
    def __init__(self, id, title, picture):
        self.id = id
        self.title = title
        self.picture = picture

def get_trending_movies(x=10):
    movie_ids = []
    r =requests.get(os.getenv('DB_URL')+"/movies/popular")
    print(r.status_code)
    if(r.status_code == 200):
        i=0
        for entry in r.json():
            i+=1
            movie_id = entry['movie_id']
            movie_ids.append(movie_id)
            if i == x:
                break
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