import click
import pandas as pd
from flask.cli import with_appcontext
from app.models import Movies


@click.command("insert-db")
@with_appcontext
def insert_db():
    """Insère les données nécessaire à l'utilisation de l'application"""

    movies = pd.read_csv("data/Movies.csv")

    Movies.Movie.insert_from_pd(movies)

    print("Données insérées !!")

