from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

db = SQLAlchemy()
installed_apps = []
mail = Mail()
bcrypt = Bcrypt()
migrate = Migrate()
