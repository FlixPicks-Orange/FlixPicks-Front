from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///survey_responses.db'
db = SQLAlchemy(app)

subscriptions = [{"Name":"Netflix", "image":"static/images/netflix.png"},
                 {"Name": "MAX", "image": "static/images/max.png"},
                 {"Name": "Disney+", "image": ""},
                 {"Name": "Prime Video", "image": ""},
                 {"Name": "Hulu", "image": ""},

                 ]

movies = [{"Name": "Dune", "image": ""},
          {"Name": "The Matrix", "image": ""},                 
          {"Name": "Barbie", "image": ""},                
          {"Name": "Friday", "image": ""},
]

@app.route('/tasteProfile', methods=['GET','POST'])
def tasteProfile():
     if request.method =='POST':
         return redirect(url_for('thank_you'))
     else:
              return render_template('tasteProfile.html', subscriptions=subscriptions, movies=movies)

@app.route('/thanks') #Eventually edit this- should redirect to homepage of FP
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    db.create_all() # Create the necessary fatabase tables
    app.run(debug=True)
