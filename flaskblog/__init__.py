from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_migrate import Migrate

# configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'f13b194786abc813d7b007bb56fad163'
# Creating a database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://fyxlflqu:6N7SBz2TTk2LdL84gFwRVwl7TDfxvldE@ziggy.db.elephantsql.com:5432/fyxlflqu'
db = SQLAlchemy(app)
# migrate = Migrate(app, db)
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


