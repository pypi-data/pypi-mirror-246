from flask import Flask, request, redirect, url_for, abort, g
from flask_login import LoginManager
from pathlib import Path
from http import HTTPStatus

from . import user
from . extensions import db, bcrypt, mail, migrate, installed_apps

installed_apps.append(user)

def create_app(instance_folder, template_folder, blueprint_groups):
    app = Flask(__name__, instance_path=instance_folder)
    app.config.from_pyfile(instance_folder / 'config.py')
    app.template_folder = template_folder

    instance_path = Path(app.instance_path)
    parent_directory = Path(instance_path.parent)
    if not parent_directory.is_dir():
        parent_directory.mkdir()
    
    if not instance_path.is_dir():
        instance_path.mkdir()
    
    
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return user.User.query.get(user_id)

    @login_manager.unauthorized_handler
    def unauthorized():
        if request.blueprint == 'api':
            abort(HTTPStatus.UNAUTHORIZED)
        return redirect(url_for('user.login'))
    
    
    # Register Blueprints
    for group in blueprint_groups:
        for module_name in dir(group):
            module = getattr(group, module_name)
            if hasattr(module, "bp"):
                installed_apps.append(module)

    menu_list = []
    for module in installed_apps:
        app.register_blueprint(getattr(module, "bp"))
        if hasattr(module, "menu_label"):
            menu_list.append(getattr(module, "menu_label"))

    app.config['MENUS'] = menu_list



    # Initialize the database
    bcrypt.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app=app, db=db)
    
    return app
