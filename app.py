
from flask import render_template, url_for, redirect, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
import random, requests, os

# Custom Modules
from config  import app
import forms, users, login_manager
from hotpicks import get_trending_movies
from recommendationCollector import getRecommendations
from getmovie import getmovie
from search import search_for_movie
from tasteProfile import get_survey_movies
from tasteProfile import get_survey_subscription
from search import search_for_movie
import Survey


# search = search_for_movie()
trending_movies = get_trending_movies(12)
survey_subs = get_survey_subscription()
survey_movies = get_survey_movies()


@app.route('/')
def home():
    return render_template('index.html', trending_movies = trending_movies)

@app.route('/search', methods=['GET' , 'POST'])
def search():
    if request.method == 'POST':
        title = request.form["movie_title"]
        search_results = search_for_movie(title)
        return  render_template('search.html', search_results = search_results)



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
    recMovies = getRecommendations(current_user.id)
    if(current_user.survey_check==False):
        return redirect(url_for('tasteProfile'))
    else:
        return render_template('userhome.html', user=current_user, trending_movies=trending_movies, recMovies = recMovies)


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


@app.route('/mediaInfo/<int:movie_id>', methods=['GET' , 'POST'])
def mediaInfo(movie_id):
    movie = getmovie(movie_id)
    return render_template('mediaInfo.html',  movie_id=movie_id, movie=movie)


@app.route('/settings', methods=['GET', 'POST', 'PATCH'])
@login_required
def settings():
    if request.method == 'PATCH':
        sub = {'limit_subscriptions': True}
        r = requests.patch(os.getenv('DB_URL') + "/users/update/" + current_user.username + "/limit_subscriptions", json=sub)
        if r.status_code == 201:
            return "Success", 201
        else:
            return "Failed", r.status_code
    return render_template('settings.html')



@app.route('/logout', methods = ['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


# @app.route('/tasteProfile', methods = ['GET','POST']) # Old tasteProfile... not sure what needs to be moved to the new one
# # @login_required
# def tasteProfile():
#     form = Survey.SurveyForm()
#     if request.method == 'POST':
#         Survey.InsertResponse
#         selected_subscriptions = request.form.getlist('subscriptions')
#         selected_movies = request.form.getlist('movies')
#         return redirect(url_for('thank_you'))
#     else:
#      return render_template('tasteProfile.html', form=form)

@app.route('/tasteProfile', methods=['GET','POST'])
def tasteProfile():
     if request.method =='POST':
        return redirect(url_for('thank_you'))
     else:
        return render_template('tasteProfile.html', subscriptions=survey_subs, movies=survey_movies)


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

# @app.route('/cineroll')
# @login_required
# def cineroll():
#      recMovies = getRecommendations(current_user.id)
#      if(len(recMovies)>1):
#          x = random.randint(0,len(recMovies))
#          movie = getmovie(recMovies[x])
#          movie_id = recMovies[x].id
#          return render_template('mediaInfo.html',  movie_id=movie_id, movie=movie)
#      else:
#           return "Movie not found", 404
        

if __name__ == '__main__':
    #Survey.db.create_all()
    app.run(host="0.0.0.0", port=2000, debug=True)

