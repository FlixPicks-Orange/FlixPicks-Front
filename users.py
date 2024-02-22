from flask_login import login_user, login_required, logout_user
import os, requests

# Custom Modules
from config import bcrypt


def username_exists(username):
    r = requests.get(os.getenv('DB_URL') + "/users/username/" + username)
    if(r.status_code == 200): return True
    else: return False


def email_exists(email):
    r = requests.get(os.getenv('DB_URL') + "/users/email/" + email)
    if(r.status_code == 200): return True
    else: return False


def get_by_id(id):
    r = requests.get(os.getenv('DB_URL') + "/users/" + id)
    if(r.status_code == 200): return r.json()
    else: return None


def get_by_username(username):
    r = requests.get(os.getenv('DB_URL') + "/users/username/" + username)
    if(r.status_code == 200): return r.json()
    else: return None


def create_user(email, username, password, fname, lname):
    if not username_exists(username) and not email_exists(email):
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        new_user = {
            'username' : username,
            'email' : email,
            'password' : hashed_password,
            'fname' : fname,
            'lname' : lname,
            'role' : 'Standard'
        }
        r = requests.post(os.getenv('DB_URL') + "/users", json=new_user)
        if(r.status_code == 201): return True
        else: return False
    else: return False

def update_login_date(username):
    r = requests.patch(os.getenv('DB_URL') + "/users/update/" + username + "/last_login")
    if(r.status_code == 201): return True
    else: return False
    
def update_survey_check(username):
    r = requests.patch(os.getenv('DB_URL') + "/users/update/" + username + "/survey_check")
    if(r.status_code == 201): return True
    else: return False

def verify_user(username, password):
    user = get_by_username(username)
    if user is None: 
        return None
    if bcrypt.check_password_hash(user["password"], password):
        update_login_date(username)
        return user
    else: 
        return None