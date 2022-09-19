from pandas import DataFrame
from app.db import db


class Movie(db.Model):
    """Movie model"""

    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    img = db.Column(db.String(255), nullable=False, unique=False)
    name = db.Column(db.String(255), unique=True, nullable=False)
    release = db.Column(db.String(20), nullable=False)
    runtime = db.Column(db.String(255), index=False, unique=False, nullable=True)
    genre = db.Column(db.String(255), index=False, unique=False, nullable=True)
    rating = db.Column(db.Float, index=False, unique=False, nullable=True)

    def insert_from_pd(self: DataFrame):
        self.to_sql("movies", db.engine, if_exists="append", index=False)
