
from flask import render_template, url_for, redirect, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
import random, requests, os

# Custom Modules
from config  import app, bcrypt
import forms, users, login_manager
from hotpicks import get_trending_movies
from recommendationCollector import getRecommendations
from getmovie import getmovie
from search import search_for_movie
# from tasteProfile import get_survey_movies
from tasteProfile import get_survey_subscription
import Survey
from analytics import most_watched, click_data
from interactions import click,postLike, postDislike
from watch_history import get_watched_movies, get_rated_movies, create_movies
from subscriptions import get_subscriptions, delete_subscription, add_subscription
survey_subs = get_survey_subscription()
# survey_movies = get_survey_movies()
header = 'header_guest.html'





@app.route('/')
def home():
    # HotPicks movie collection, then passed to the html template and displayed to user
    trending_movies = get_trending_movies()
    return render_template('index.html', header = header, trending_movies = trending_movies)


@app.route('/search', methods=['GET' , 'POST'])             
def search():
    if request.method == 'POST':
        title = request.form["movie_title"]
        search_results = search_for_movie(title)
        if current_user.is_authenticated:
            header = 'header_registered.html'
        else:
            header = 'header_guest.html'
        return  render_template('search.html', header = header, search_results = search_results)

@app.route('/wheelresult', methods=['GET','POST'])
def wheelresult():
    if request.method == 'POST':
        title = request.form["movie_title"]
        search_results = search_for_movie(title)
        if current_user.is_authenticated:
            header = 'header_registered.html'
        else:
            header = 'header_guest.html'
        return  render_template('search.html', header = header, search_results = search_results )
    else: return(redirect(url_for('wheel'))) # This line redirects user back to wheel input if nothing was posted

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
            return render_template('login.html', header = header, form=form, error_message=error_message)
    return render_template('login.html', header = header, form=form)


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
    return render_template('register.html', header = header, form = form)


@app.route('/userhome', methods=['GET' , 'POST'])
@login_required
def userhome():
    #Recommended movie collection based on user id (recommendationCollector.py)
    recMovies = getRecommendations(current_user.id)
    trending_movies = get_trending_movies()
    if(current_user.survey_check==False):
        return redirect(url_for('tasteProfile'))
    else:
        return render_template('userhome.html', header = 'header_registered.html', user=current_user, trending_movies=trending_movies, recMovies=recMovies if recMovies else [])



@app.route('/mediaInfo/<int:movie_id>', methods=['GET' , 'POST'])             
def mediaInfo(movie_id):
    movie = getmovie(movie_id)
    if current_user.is_authenticated:
        header = 'header_registered.html'
    else:
        header = 'header_guest.html'
    
    if request.method =='POST' and current_user.is_authenticated:
        movie = { 
            "from_recommended": True,
            "movie_id":movie_id,
            "user_id": current_user.id
            }

        r = requests.post(os.getenv('DB_URL') + f"/watch_history", json=movie)
        if r.status_code == 201:
            print('Succesfully updated Watch History.')
        
    return render_template('mediaInfo.html', header = header,  movie_id=movie_id, movie=movie)


@app.route('/settings', methods=['GET', 'POST', 'PATCH', 'DELETE'])
@login_required
def settings():
    subs = get_subscriptions(current_user.id)
    #Update password, PATCH request triggers 
    if request.method == 'PATCH':
         if 'newPassword' in request.json and 'confirmPassword' in request.json:
            new_password = request.json['newPassword']
            confirm_password = request.json['confirmPassword']
            
            if new_password != confirm_password:
                return "New password and confirmed password do not match", 400

            updated_password = bcrypt.generate_password_hash(new_password).decode("utf-8")
            updated_password = {'password': updated_password}
            r_password = requests.patch(os.getenv('DB_URL') + f"/users/update/{current_user.username}/password", json=updated_password)

            if r_password.status_code == 200:
                return "Password updated successfully", 200
            else:
                return "Failed to update password", 404
    #Delete subscription services
    elif request.method == 'DELETE':
        if 'provider_id' in request.json:
            provider_id = request.json['provider_id']
            delete_subscription(current_user.id, provider_id)
            return "Subscription deleted successfully", 200
        else:
            return "Missing provider_id in request", 400
    #Add subscription services
    elif request.method == 'POST':
        if 'provider_id' in request.json:
            provider_id = request.json['provider_id']
            add_subscription(current_user.id, provider_id)
            return "Subscription added successfully", 201
        else:
            return "Missing provider_id in request", 400
    elif request.method == 'GET' or request.method == 'POST':
        return render_template('settings.html', header='header_registered.html', subs=subs)



@app.route('/logout', methods = ['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/tasteProfile', methods=['GET','POST'])
@login_required
def tasteProfile():
     trending_movies = get_trending_movies()

     if request.method =='POST':
        subscriptions = request.form.getlist("subscriptions")
        trending_movies = request.form.getlist("trending_movies")
        for subscription in subscriptions : 
            r = requests.post(os.getenv("DB_URL")+f"/subscriptions/{current_user.id}/update/{subscription}")
        for movie_id in trending_movies :
            movie = { 
            "from_recommended": False,
            "movie_id": int(movie_id),
            "user_id": current_user.id
            }
            r = requests.post(os.getenv('DB_URL') + f"/watch_history", json=movie)
            if r.status_code == 201:
                print('Succesfully updated Watch History.')
            else:
                print('Get good scrub')
        return redirect(url_for('thank_you')) 
     else:
         return render_template('tasteProfile.html', header = header, trending_movies = trending_movies, subscriptions = survey_subs)


@app.route('/thanks') #Eventually edit this- should redirect to homepage of FP
def thank_you():
    users.update_survey_check(current_user.username)
    return render_template('thankyou.html', header = header)


@app.route('/survey_results')
def survey_results():
    # Retrieve all survey responses from the database
    all_responses = Survey.SurveyResponse.query.all()
    response_list = [{'id': response.id, 'question': response.question, 'response': response.response} for response in all_responses]
    return jsonify(response_list)

@app.route('/wheel')
def wheel():
    if current_user.is_authenticated:
            header = 'header_registered.html'
    else:
        header = 'header_guest.html'
    return render_template('wheel.html', header  = header)

@app.route('/cineroll')
@login_required
def cineroll():
    recMovies = getRecommendations(current_user.id)
    if(len(recMovies)>1):
        x = random.randint(0,len(recMovies))
        movie_id = recMovies[x].id
        movie = getmovie(movie_id)
        return render_template('mediaInfo.html', header = 'header_registered.html',  movie_id=movie_id, movie=movie)
    else:
        return "Movie not found", 404
     
@app.route('/watch_history', methods=['GET' , 'POST'])
@login_required
def watch_history():
    watched = reversed(get_watched_movies(current_user.id))
    liked_ids, disliked_ids = get_rated_movies(current_user.id)
    liked = reversed(create_movies(liked_ids))
    disliked = reversed(create_movies(disliked_ids))
    return render_template('watch_history.html', header = 'header_registered.html', user=current_user, watched=watched, liked=liked, disliked=disliked)

@app.route('/test')
def test():
    return render_template('analytics.html', plot_url=most_watched(5))  

@app.route('/add_click', methods=['POST'])
def add_click():
    data = request.json
    num_clicks = data.get('num_clicks')
    page_url = data.get('page_url')
    if  current_user.is_authenticated:
        user_id = current_user.id
    else:
        user_id = 100

    return click(num_clicks, page_url, user_id)      

@app.route('/like', methods=['POST'])
def like():
    data = request.json
    movie_id = data.get('movie')
    if  current_user.is_authenticated:
        user_id = current_user.id
    else:
        user_id = 100
    package = {
        'movie_id': movie_id,
        'user_id': user_id,
        'user_liked': True
    }
    return postLike(package, user_id, movie_id)

@app.route('/dislike', methods=['POST'])
def dislike():
    data = request.json
    movie_id = data.get('movie')
    if  current_user.is_authenticated:
        user_id = current_user.id
    else:
        user_id = 100
    package = {
        'movie_id': movie_id,
        'user_id': user_id,
        'user_liked': True
    }
    return postDislike(package, user_id, movie_id)

if __name__ == '__main__':
    #Survey.db.create_all()
    app.run(host="0.0.0.0", port=2000, debug=True)

# Wheel output handler needed