
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
from flask_babel import Babel
from dotenv import load_dotenv

load_dotenv()

app = Flask(
    __name__,
    template_folder= os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'),
    static_folder= os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
)

app.config['BABEL_DEFAULT_LOCALE'] = 'es'
app.config['LANGUAGES'] = [
    'en',
    'es',
    'gl',
]

babel = Babel(app)

postgres_user = os.getenv('POSTGRES_USER')
postgres_password = os.getenv('POSTGRES_PASSWORD')
postgres_host = os.getenv('POSTGRES_HOST')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{postgres_user}:{postgres_password}@{postgres_host}:5432/notlar'
app.config['SECRET_KEY'] = 'your_secret_key_here'

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = '/'
login_manager.init_app(app)

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'img', 'users')

if not os.access(UPLOAD_FOLDER, os.W_OK):
    print("Upload folder does not have write permissions!")

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


from notlar import routes, models, auth

