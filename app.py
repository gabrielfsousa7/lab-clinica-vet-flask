import click
from flask import Flask
from flask.cli import with_appcontext
from flask_login import LoginManager, login_manager
from flask_migrate import Migrate
from database import db
from models import User, Tutor, Pet, Agendamento


def create_app():
    app = Flask(__name__)
    app.secret_key = "abax"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dados.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    db.init_app(app)
    Migrate(app, db)

    app.cli.add_command(init_db_command)
    app.cli.add_command(create_admin_user)

    @login_manager.user_loader
    def load_user(user_id: str):
        return User.query.filter_by(id=int(user_id)).first()

    from auth import bp as auth_bp
    from ctrl_home import bp as home_bp
    from controller import bp as main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(main_bp)

    return app


def init_db():
    db.drop_all()
    db.create_all()


@click.command("createsuperuser")
@with_appcontext
def create_admin_user():
    from getpass import getpass
    from auth import create_user

    create_user(getpass("Digite a senha para admin: "))


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database.")


if __name__ == "__main__":
    create_app().run(debug=True, host="0.0.0.0")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(id=int(user_id)).first()