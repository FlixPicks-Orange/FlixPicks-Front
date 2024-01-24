from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

questions = [
    "What are your favorite genres?"
    "When do you watch TV?"
    "Do you prefer light-hearted movies or more serious ones?"
    "Live Action or Animation?"
    "Quick binge or Slow burn?"
    "What do you pay attention to most in movies?"
    "Who do you typically watch TV with?"
    "How often to you watch movies?"
    "Why do you watch TV?"
    "What is your go-to streaming service?"
        #Add more questions here if needed
]

@app.route('/')
def index():
    return render_template('tasteProfile.html') #This is basically rerouting to show
                                                #the taste profile survey on the screen

@app.route('/submit', methods=['POST'])
def submit():
    responses = [request.form[str(i)] for i in range(1, len(questions) +1)]
    #TESTING CODE START
    print(responses) #Print the responses just to make sure that they
                     #Are being read correctly
    
@app.route('/thanks') #Eventually edit this- should redirect to homepage of FP
def thank_you():
    return "Thank you for completing the Taste Survey!" #Cuter message -> redirect to FP

if __name__ == '__main__':
    app.run(debug=True)