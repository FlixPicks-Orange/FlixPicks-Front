from flask import render_template, url_for, redirect, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
import random

# Custom Modules
from config  import app
import forms, users, login_manager
from hotpicks import get_trending_movies
import Survey



trending_movies = get_trending_movies(12)


@app.route('/')
def home():
    return render_template('index.html', trending_movies = trending_movies)


@app.route('/hotpicks/<int:movie_id>')
def hotpicks(movie_id):
    selected_movie = None
    for movie in trending_movies:
        if movie.id == movie_id:
            selected_movie = movie
            break
    if selected_movie:
        return render_template('hotpicks.html', movie=selected_movie)
    else:
        return "Movie not found", 404


@app.route('/login', methods=['GET' , 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = users.verify_user(form.username.data, form.password.data)
        if user is not None:
            login_user(login_manager.User(user))
            return(redirect(url_for('userhome')))
        else:
            error_message = 'Login failed. Please check your credentials.'
            return render_template('login.html', form=form, error_message=error_message)
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET' , 'POST'])
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        result = users.create_user(
            form.email.data, 
            form.username.data, 
            form.password.data,
            form.fname.data,
            form.lname.data
            )
        if(result): return redirect(url_for('login'))
    return render_template('register.html', form = form)


@app.route('/userhome', methods=['GET' , 'POST'])
@login_required
def userhome():
    if(current_user.survey_check==False):
        return redirect(url_for('tasteProfile'))
    else:
        return render_template('userhome.html', user=current_user, trending_movies=trending_movies)


@app.route('/spin', methods=['POST'])
def spin():
    options = request.form.get('options')
    if not options:
        return "Please enter at least one option."
    
    options_list = options.split(',')
    selected_option = random.choice(options_list)
    return render_template('result.html', selected_option=selected_option)


@app.route('/result', methods=['POST'])
def result():
    options = request.form.getlist('option')
    selected_option = random.choice(options)
    return render_template('result.html', selected_option=selected_option)


@app.route('/mediaInfo/<int:page_id>', methods=['GET' , 'POST'])
@login_required
def mediaInfo(page_id):
    return render_template('mediaInfo.html',  page_id=page_id)


@app.route('/logout', methods = ['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


# TASTE PROFILE STUFF FROM "Survey.py"

@app.route('/tasteProfile', methods = ['GET','POST'])
@login_required
def tasteProfile():
    form = Survey.SurveyForm()
    if request.method == 'POST':
        Survey.InsertResponse({
            "data": [
                {'label':form.q1.label.text, 'option':form.q1.data},
                {'label':form.q2.label.text, 'option':form.q2.data},
                {'label':form.q3.label.text, 'option':form.q3.data},
                {'label':form.q4.label.text, 'option':form.q4.data},
                {'label':form.q5.label.text, 'option':form.q5.data},
                {'label':form.q6.label.text, 'option':form.q6.data},
                {'label':form.q7.label.text, 'option':form.q7.data},
                {'label':form.q8.label.text, 'option':form.q8.data},
                {'label':form.q9.label.text, 'option':form.q9.data},
                {'label':form.q10.label.text, 'option':form.q10.data},
                {'label':form.q11.label.text, 'option':form.q11.data},
            ]
        })
        return redirect(url_for('thank_you'))
    return render_template('tasteProfile.html', form=form)


@app.route('/thanks') #Eventually edit this- should redirect to homepage of FP
def thank_you():
    users.update_survey_check(current_user.username)
    return render_template('thankyou.html')


@app.route('/survey_results')
def survey_results():
    # Retrieve all survey responses from the database
    all_responses = Survey.SurveyResponse.query.all()
    response_list = [{'id': response.id, 'question': response.question, 'response': response.response} for response in all_responses]
    return jsonify(response_list)

@app.route('/wheel')
def wheel():
    return render_template('wheel.html')

if __name__ == '__main__':
    #Survey.db.create_all()
    app.run(host="0.0.0.0", port=2000, debug=True)

