import pandas as pd
import matplotlib.pyplot as plt
import os, json, requests
import io, base64
def most_watched(number):
    r = requests.get(os.getenv('DB_URL') + "/watch_history")
    data = r.json()
    movie_counts = {}
    for entry in data:
        movie_id = entry['movie_id']
        k = requests.get(os.getenv('DB_URL') + "/movies/" + str(movie_id))
        package = k.json()
        movie = package[0]
        title = movie['title']
        count = 1
        if title in movie_counts:
            count = movie_counts[title]
            count = count + 1
            movie_counts[title] = count
        else:
            movie_counts[title] = count
    p = requests.get(os.getenv('DB_URL')+ "/watch_history/titles")
    if p.status_code == 200:
        with_titles = p.json()
        print(with_titles)
    df_movie_counts = pd.DataFrame(list(movie_counts.items()), columns=['title', 'count'])
    df_top_counts = df_movie_counts.nlargest(number, 'count')
    plt.bar(df_top_counts['title'], df_top_counts['count'], color='blue')
    plt.xlabel('Movie Title')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    #print(plot_url)
    plt.close()
    return plot_url
    dict_top_movies = df_top_counts.to_dict(orient='records')
    return dict_top_movies
    
