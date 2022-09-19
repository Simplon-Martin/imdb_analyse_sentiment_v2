import os
from flask import Flask
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
import yaml
from app.controllers.controller import main
from app.db import db
from app.commands import insert_db
from app import auth, main
from app.models import User, Movies, Rating


def create_app(test_config=None):
    # On initialise l'app flask
    app = Flask(__name__, instance_relative_config=True)

    app.config['SECRET_KEY'] = '\xaf\xdc\xea\x06{\xc1[$f\xa4Z\x00\x15\xe1\xf8\x87\xc7\xc5\xc6\x19\xd2:\xb3]'

    # On initialise flask-migrate pour les outils de migration de la BDD
    migrate = Migrate()

    # Configuration de l'application
    # On récupère en premier la configuration d'un fichier config.yaml présent dans /instance/config.yml
    # Tout d'abord on vérifie que le fichier config.yml est bien présent dans le dossier instance
    if os.path.isfile(app.instance_path + "/config.yml"):
        # S'il est présent, on charge la configuration de celui-ci dans l'app flask
        app.config.from_file("config.yml", load=yaml.safe_load)
        # Dans le cas où DEFAULT_DB est bien présent dans la config, on met en place la configuration de SQLAlchemy
        # en fonction des éléments présents dans config.json
        if "DEFAULT_DB" in app.config:
            # On récupère la config de la base de données à utiliser par défaut du config.json
            dbconfig = app.config[app.config["DEFAULT_DB"]]
            app.config.from_mapping(
                {
                    "SQLALCHEMY_DATABASE_URI": f"{dbconfig['connector']}://{dbconfig['user']}:{dbconfig['password']}@{dbconfig['host']}:{dbconfig['port']}/{dbconfig['bdd']}",
                    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
                }
            )
    else:
        # Au cas où il n'existe pas, on avertit que celui-ci n'est pas présent
        app.logger.warning(
            "Aucun fichier config.yml n'est présent dans le dossier /instance/. L'application risque de mal "
            "fonctionner ! "
        )

    # Si la variable d'environnement (défini via terminal ou dans le fichier .env à la racine du dossier)
    # DATABASE_URL existe On remplace la config de connexion à la base de données par cette variable environnment
    if "DATABASE_URL" in os.environ:
        app.config.from_mapping(
            {
                "SQLALCHEMY_DATABASE_URI": os.environ["DATABASE_URL"].replace(
                    "postgres://", "postgresql+psycopg2://"
                )
            }
        )

    # Dans le cas de tests, on passe directement la configuration à create_app, la config de test doit donc remplacer
    # toutes les configs précédentes
    if test_config is not None:
        app.config.from_mapping(test_config)

    # On initialise la configuration de connexion à la bdd
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.User.query.get(int(user_id))

    # On initialise l'outil de migration
    migrate.init_app(app, db)

    # On ajoute la commande "flask insert-db" à l'application
    app.cli.add_command(insert_db)

    # On initialise bootstrap
    Bootstrap(app)

    # blueprint for auth routes in our app
    app.register_blueprint(auth.auth)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
