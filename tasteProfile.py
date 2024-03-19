from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///survey_responses.db'
db = SQLAlchemy(app)

subscriptions = [{"Name":"Netflix", "images":"static/images/netflix.png"}]

movies = ["Dune", "The Matrix", "Spider-Man: No Way Home","Bridesmade"]

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
