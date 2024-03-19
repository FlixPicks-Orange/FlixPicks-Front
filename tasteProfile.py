from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///survey_responses.db'
db = SQLAlchemy(app)

def get_survey_subscription() :
    subscriptions = [{"Name":"Netflix", "image":"../static/images/netflix.png"},
                {"Name": "MAX", "image": "../static/images/max.png"},
                {"Name": "Disney+", "image": "../static/images/disney+.png"},
                {"Name": "Prime Video", "image": "../static/images/prime_video.png"},
                {"Name": "Hulu", "image": "../static/images/hulu.jpg"},
                ]
    return subscriptions

def get_survey_movies() :
    movies = [{"Name": "Dune", "image": "../static/images/dune_poster.png"},
        {"Name": "The Matrix", "image": "../static/images/matrix_poster.jpg"},
        {"Name": "Barbie", "image": "../static/images/barbie_movie_poster.jpg"},
        {"Name": "Friday", "image": "../static/images/friday_poster.jpg"},
    ]
    
    return movies