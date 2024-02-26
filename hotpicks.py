import requests

api_key = "250af020182447c7468c03c9ec6cb7a2"

class Movie:
    def __init__(self, title, url, release_date, picture):
        self.title = title
        self.url = url
        self.release_date = release_date
        self.picture = picture

def get_trending_movies(num_movies=10):
    url = f"https://api.themoviedb.org/3/trending/movie/week?api_key={api_key}"
    response = requests.get(url)
    trending_movies = []
    if response.status_code == 200:
        movies_data = response.json().get('results', [])
        for movie_data in movies_data[:num_movies]:
            title = movie_data.get('title', 'Title not available')
            release_date = movie_data.get('release_date', 'Release date not available')
            picture = f"https://image.tmdb.org/t/p/w500{movie_data.get('poster_path', '')}"
            url = f"https://www.themoviedb.org/movie/{movie_data.get('id')}"
            movie = Movie(title, url, release_date, picture)
            trending_movies.append(movie)
    else:
        print("Error fetching data:", response.status_code)
    return trending_movies



