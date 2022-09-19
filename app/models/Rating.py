import datetime
from app.db import db


class Rating(db.Model):
    """Rating model"""

    __tablename__ = "ratings"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column("movie_id", db.Integer, db.ForeignKey('movies.id'), nullable=False)
    review = db.Column("review", db.Text, nullable=False)
    rating = db.Column("rating", db.Float, nullable=False)
    created_at = db.Column("created_at", db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, index=False, unique=False, nullable=True)




