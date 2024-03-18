from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# Configuring the SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///survey_responses.db'
db = SQLAlchemy(app)

# Define the model for survey responses
class SurveyResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    response = db.Column(db.String(255), nullable=False)

questions = {
    "What are your favorite genres?":["Horror","Fantasy","Action","Drama","Comedy","Romance","Other"],
    "When do you watch movies or TV?":["In the morning, while eating breakfast","In the afternoon, during lunch","At night, after work"],
    "Do you prefer light-hearted movies or more serious ones?": ["Light-hearted","Serious and dramatic"],
    "Live action or animation?":["Live Action","Animation"],
    "Do you like to binge watch or to take your time?":["Binge watch","Take my time"],
    "What do you pay attention to most in movies?":["The acting","The plot","The action","Everything"],
    "Who do you typically watch TV with?":["By myself","With friends","With family"],
    "How often to you watch movies?":["Hardly at all","A couple times a month","A couple times a week","Every day"],
    "Why do you watch TV?":["To keep up with trending media","For relaxation","For entertainment"],
    "What is your preferred streaming service?":["Netflix","Hulu","MAX","Prime Video","Paramount+","Other"],
    "Are you subscribed to any streaming services?":["None","One","Two","Three","Four or more"]
        #Add more questions here if needed
}



@app.route('/submit', methods=['POST'])
def submit():
    # Iterate through each question and its corresponding response
    for i in range(1, len(questions) + 1):
        question = list(questions.keys())[i - 1]
        response = request.form[str(i)]
   

    # Save the response to the database
        survey_response = SurveyResponse(question=question, response=response)
        db.session.add(survey_response)

    # Commit changes to the database
    db.session.commit()

    return redirect(url_for('thank_you'))
    
@app.route('/thanks') #Eventually edit this- should redirect to homepage of FP

def thank_you():
    return "Thank you for completing the Taste Profile survey!" #Cuter message -> redirect to FP
    # return redirect(url_for('userhome')) - maybe?

@app.route('/survey_results')
def survey_results():
    # Retrieve all survey responses from the database
    all_responses = SurveyResponse.query.all()
    return render_template('surveyResults.html', responses=all_responses)


if __name__ == '__main__':
    db.create_all() # Create the necessary fatabase tables
    app.run(debug=True)
