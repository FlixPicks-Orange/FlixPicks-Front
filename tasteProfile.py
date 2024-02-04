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
    "What are your favorite genres?":["Horror","Fantasy","Action","Drama","Comedy","Other"],
    "When do you watch TV?":["In the morning, while eating breakfast","In the afternoon, during lunch","At night, after work"],
    "Do you prefer light-hearted movies or more serious ones?": ["Light-hearted","Serious and dramatic"],
    "Live Action or Animation?":["Live Action","Animation"],
    "Do you like a quick binge or to take your time?":["Quick binge","Take my time"],
    "What do you pay attention to most in movies?":["The acting","The plot","Everything"],
    "Who do you typically watch TV with?":["By myself","With friends","With family"],
    "How often to you watch movies?":["Hardly at all","Rarley","Time to Time","Almost every day"],
    "Why do you watch TV?":["To keep up with trending media","To relax","To relieve boredem"],
    "What is your go-to streaming service?":["Netflix","Hulu","MAX","Prime Video","Paramount+","Other"]
        #Add more questions here if needed
}

@app.route('/')
def index():
    return render_template('tasteProfile.html') #This is basically rerouting to show
                                                #the taste profile survey on the screen

@app.route('/submit', methods=['POST'])
def submit():
    # Iterate through each question and its corresponding response
    for i in range(1, len(questions) + 1):
        question = list(questions.keys())[i - 1]
        response = request.form[str(i)]
    #(OLD) responses = [request.form[str(i)] for i in range(1, len(questions) +1)] 

    # Save the response to the database
        survey_response = SurveyResponse(question=question, response=response)
        db.session.add(survey_response)

    # Commit changes to the database
    db.session.commit()
    
    #TESTING CODE START
    print(responses) #Print the responses just to make sure that they
                     #Are being read correctly
    #TESTING CODE END
@app.route('/thanks') #Eventually edit this- should redirect to homepage of FP

def thank_you():
    return "Thank you for completing the Taste Survey!" #Cuter message -> redirect to FP

if __name__ == '__main__':
    db.create_all() # Create the necessary fatabase tables
    app.run(debug=True)
