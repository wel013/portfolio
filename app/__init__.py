from flask import Flask, abort
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager, current_user
from functools import wraps
import os

from flask import Flask, abort
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager, current_user
from functools import wraps
import os
db = SQLAlchemy()
ckeditor = CKEditor()
bootstrap = Bootstrap5()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='your_secret_key',
        SQLALCHEMY_DATABASE_URI='sqlite:///your_database.db',  # Using instance_path
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    db.init_app(app)
    ckeditor.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)

    @login_manager.user_loader
    def load_user(user_id):
        return db.get_or_404(User, user_id)

    def admin_only(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.id == 1:
                return f(*args, **kwargs)
            else:
                return abort(403)
        return wrapped

    with app.app_context():
        from . import routes, models
        db.create_all()

    return app
