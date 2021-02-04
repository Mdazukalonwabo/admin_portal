from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# CONGIFIGURATIONS
app = Flask(__name__)
app.config['SECRET_KEY'] = 'f13b194786abc813d7b007bb56fad163'
# Creating a database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://sbsghgfk:cLnUBFytdp_RuQR25R6YloO3mnUIgQGl@raja.db.elephantsql.com:5432/sbsghgfk'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)   # manages login sessions
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


from flaskblog.users.routes import users
from flaskblog.main.routes import main
from flaskblog.automation.routes import automation

app.register_blueprint(users)
app.register_blueprint(main)
app.register_blueprint(automation)

db.create_all()
db.session.commit()


