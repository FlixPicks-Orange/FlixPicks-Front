from flask_login import UserMixin, LoginManager

# Custom Modules
from config  import app
import users

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, user_json):
        self.user_json = user_json
        self.id = user_json.get('id')
        self.username = user_json.get('username')
        self.fname = user_json.get('fname')
        self.lname = user_json.get('lname')
        self.last_login = user_json.get('last_login')
        self.survey_check = user_json.get('survey_check')

    
    def get_id(self):
        object_id = self.user_json.get('id')
        return str(object_id)

@login_manager.user_loader
def load_user(user_id):
    return User(users.get_by_id(user_id))