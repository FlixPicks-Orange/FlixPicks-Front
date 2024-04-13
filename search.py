import requests, os

class Movie:
    def __init__(self, id, title, release_date, picture):
        self.id = id
        self.title = title
        self.release_date = release_date
        self.picture = picture
        # add summary

def search_for_movie(title):
    r = requests.get(os.getenv("DB_URL")+"/movies/by_title/"+title)
    searches = []
    if(r.status_code==200):
        search_results = r.json()
        for item in search_results:
            id = item['movie_id']
            title =  item['title']
            release_date =  item['release_date']
            picture =  item['poster_path']
            movie = Movie(id, title, release_date, picture)
            searches.append(movie)
    else :
        print("Error fetching data:", r.status_code)
    return searches
    
# def get_list_of_movie_titles():
#     r = requests.get(os.getenv("DB_URL")+"/movies/get_titles")
#     if(r.status_code==200):
#         return r.json()
#     else :
#         return None

def get_trending_movies(num_movies=12):
    url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={api_key}"
    response = requests.get(url)
    trending_movies = []
    if response.status_code == 200:
        movies_data = response.json().get('results', [])
        for movie_data in movies_data[:num_movies]:
            id = movie_data.get('id')
            title = movie_data.get('title', 'Title not available')
            release_date = movie_data.get('release_date', 'Release date not available')
            picture = f"https://image.tmdb.org/t/p/w500{movie_data.get('poster_path', '')}"
            url = f"https://www.themoviedb.org/movie/{movie_data.get('id')}/watch"
            movie = Movie(id, title, url, release_date, picture)
            trending_movies.append(movie)
    else:
        print("Error fetching data:", response.status_code)
    return trending_movies


