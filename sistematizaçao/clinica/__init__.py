from flask import Flask,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///comunidade.db"
app.config["SECRET_KEY"] = "5702736e8a76be05c07f04654c8dc829"

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_Manager = LoginManager(app)
login_Manager.login_view = "homepage"


from clinica import routes