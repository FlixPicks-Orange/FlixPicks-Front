from flask import render_template, url_for, redirect, request
from flask_login import login_user, login_required, logout_user, current_user
import random

# Custom Modules
from config  import app
import forms, users, login_manager
from youtube import get_homepage_video_data


popular_videos = get_homepage_video_data()


@app.route('/')
def home():
    return render_template("index.html",   video1=popular_videos[0],  video2=popular_videos[1],     video3=popular_videos[2],
    video4=popular_videos[3],   video5=popular_videos[4],    video6=popular_videos[5],    video7=popular_videos[6],    video8=popular_videos[7],         video9=popular_videos[8],       video10=popular_videos[9])


@app.route('/quickclick/<int:video_id>')
def quickclick(video_id):
    video = popular_videos[video_id]
    return render_template('quickclick.html', video=video)



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
    return render_template('userhome.html', user=current_user)


@app.route('/spin', methods=['POST'])
def spin():
    options = request.form.get('options')
    if not options:
        return "Please enter at least one option."

    options_list = options.split(',')
    selected_option = random.choice(options_list)
    return render_template('result.html', selected_option=selected_option)


@app.route('/result', methods=['POSt'])
def result():
    options = request.form.getlist('option')
    selected_option = random.choice(options)
    return render_template('result.html', selected_option=selected_option)


@app.route('/mediaInfo/<int:page_id>', methods=['GET' , 'POST'])
@login_required
def mediaInfo(page_id):
    request = youtube.videos().list(
        part='snippet',
        id=page_id,
        )
    response = request.execute()
    video_info = response['items'][0]['snippet']

    video_title = video_info['title']
    video_thumbnail = video_info['thumbnails']['default']['url']
    video_url = f'https://www.youtube.com/watch?v={page_id}'

    return render_template('mediaInfo.html', video_title=video_title, video_thumbnail=video_thumbnail, video_url=video_url, page_id=page_id)


@app.route('/logout', methods = ['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=2000, debug=True)
