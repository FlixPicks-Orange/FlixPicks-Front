import pathlib
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import RadioField
from wtforms.validators import InputRequired
from config  import app

basedir = pathlib.Path(__file__).parent.resolve()
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'survey_responses.db'}"
db = SQLAlchemy(app)


class SurveyResponse(db.Model):
    __tablename__ = "responses"
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    response = db.Column(db.String(255), nullable=False)


class SurveyForm(FlaskForm):
    q1 = RadioField(label="What are your favorite genres?", 
                    choices=["Horror","Fantasy","Action","Drama","Comedy","Romance","Other"])
    q2 = RadioField(label="When do you watch movies or TV?", 
                    choices=["In the morning, while eating breakfast","In the afternoon, during lunch","At night, after work"])
    q3 = RadioField(label="Do you prefer light-hearted movies or more serious ones?", 
                    choices=["Light-hearted","Serious and dramatic"])
    q4 = RadioField(label="Live action or animation?", 
                    choices=["Live Action","Animation"])
    q5 = RadioField(label="Do you like to binge watch or to take your time?", 
                    choices=["Binge watch","Take my time"])
    q6 = RadioField(label="What do you pay attention to most in movies?", 
                    choices=["The acting","The plot","The action","Everything"])
    q7 = RadioField(label="Who do you typically watch TV with?", 
                    choices=["By myself","With friends","With family"])
    q8 = RadioField(label="How often to you watch movies?", 
                    choices=["Hardly at all","A couple times a month","A couple times a week","Every day"])
    q9 = RadioField(label="Why do you watch TV?", 
                    choices=["To keep up with trending media","For relaxation","For entertainment"])
    q10 = RadioField(label="What is your preferred streaming service?",  
                    choices=["Netflix","Hulu","MAX","Prime Video","Paramount+","Other"])
    q11 = RadioField(label="Are you subscribed to any streaming services?",  
                    choices=["None","One","Two","Three","Four or more"])
    


def InsertResponse(responses):
    for response in responses['data']:
        new_response = SurveyResponse(question=response['label'], 
                                      response=response['option'])
        db.session.add(new_response)
        db.session.commit()
    return True