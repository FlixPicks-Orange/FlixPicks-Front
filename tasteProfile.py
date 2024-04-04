from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///survey_responses.db'
db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

#  subscriptions = [{"Name":"Netflix", "image":"../static/images/netflix.svg"},
     #           {"Name": "MAX", "image": "../static/images/max.svg"},
      #          {"Name": "Disney+", "image": "../static/images/disney+.svg"},
       #         {"Name": "Prime Video", "image": "../static/images/prime_video.svg"},
        #        {"Name": "Hulu", "image": "../static/images/hulu.svg"},
         #       ]
    #return subscriptions

# def get_survey_movies() :
   # movies = [{"Name": "Dune", "image": "../static/images/dune_poster.jpg"},
      #  {"Name": "The Matrix", "image": "../static/images/matrix_poster.jpg"},
       # {"Name": "Barbie", "image": "../static/images/barbie_movie_poster.jpg"},
       # {"Name": "Friday", "image": "../static/images/friday_poster.jpg"},
    #]
    
    #return movies