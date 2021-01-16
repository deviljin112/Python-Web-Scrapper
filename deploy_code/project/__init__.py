from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()


def page_not_found(e):
    return render_template("404.html", page_name="ERROR 404")


def create_app():
    app = Flask(__name__)

    app.register_error_handler(404, page_not_found)
    app.static_folder = "static"

    app.config["SECRET_KEY"] = "4a24c55bca772e224862f6234f90ac49e0760a9d465f3ecd"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app


app = create_app()