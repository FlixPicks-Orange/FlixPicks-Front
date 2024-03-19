from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///survey_responses.db'
db = SQLAlchemy(app)

subscriptions = [{"name":"Netflix","image":"netflix.png"},
                 {"name":"Netflix","image":"netflix.png"},
                 {"name":"Netflix","image":"netflix.png"}
                ]

movies = [{"id": 1, "title": "Dune", "poster": "dune.png"},
          {"id": 1, "title": "Dune", "poster": "dune.png"},
          {"id": 1, "title": "Dune", "poster": "dune.png"}]

@app.route('/tasteProfile', methods=['GET','POST'])
def tasteProfile():
     if request.method =='POST':
         selected_subscriptions = request.form.getlist('subscriptions')
         selected_movies = request.form.getlist('movies')
         return "Form submitted"
     else:
              return render_template('tasteProfile.html', subscriptions=subscriptions, movies=movies)

@app.route('/thanks') #Eventually edit this- should redirect to homepage of FP

def thank_you():
    return "Thank you for completing the Taste Profile survey!" #Cuter message -> redirect to FP
    # return redirect(url_for('userhome')) - maybe?

#@app.route('/survey_results')
#def survey_results():
    # Retrieve all survey responses from the database
    #all_responses = SurveyResponse.query.all()
    #return render_template('surveyResults.html', responses=all_responses)


if __name__ == '__main__':
    db.create_all() # Create the necessary fatabase tables
    app.run(debug=True)
