from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from app.models import User, Movies, Rating
import datetime
import pickle

from app.db import db

main = Blueprint('main', __name__)

ROWS_PER_PAGE = 20


@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    movies = db.session.query(Movies.Movie).paginate(page=page, per_page=ROWS_PER_PAGE)
    print(movies)
    return render_template('index.html', movies=movies, page=page, current_user=current_user)


@main.route('/profile')
@login_required
def profile():
    user_ratings = db.session.query(Rating.Rating).filter(Rating.Rating.user_id == current_user.id).all()
    movies = db.session.query(Movies.Movie).all()
    return render_template('profile.html', name=current_user.name, user_ratings=user_ratings, movies=movies)


@main.route('/community_reviews')
@login_required
def community_reviews():
    movies = db.session.query(Movies.Movie).all()

    movie_ratings_by_users = {}
    for movie in movies:
        users_ratings_movie = db.session.query(Rating.Rating).filter(Rating.Rating.movie_id == movie.id).all()
        if users_ratings_movie:
            movie_ratings_by_users[movie.name] = users_ratings_movie

    print(movie_ratings_by_users)
    return render_template('commu_reviews.html',
                           name=current_user.name,
                           movie_ratings_by_users=movie_ratings_by_users,
                           movies=movies)


@main.route("/movie/<int:movie_id>", methods=['GET', 'POST'])
def find_movie(movie_id):
    movie = db.session.query(Movies.Movie).get(movie_id)
    return render_template("movie.html", movie=movie)


@main.route("/review/<int:movie_id>", methods=['GET', 'POST'])
def movie_review(movie_id):
    exist_review = db.session.query(Rating.Rating).filter(Rating.Rating.movie_id == movie_id,
                                                          Rating.Rating.user_id == current_user.id).first()
    movie = db.session.query(Movies.Movie).get(movie_id)
    return render_template("form_review.html", movie=movie, exist_review=exist_review)


@main.route("/create_review", methods=['GET', 'POST'])
def create_review():
    model = load_model()
    movie_id = request.form['movie_id']
    review = request.form['review']

    prediction = model.predict([review])
    prediction_proba = model.predict_proba([review])


    rating_score = prediction_proba[0][1]

    rating_score_on_cent = (rating_score * 10)
    format_rating_score = "{:.2f}".format(rating_score_on_cent)


    new_review = Rating.Rating(user_id=current_user.id, movie_id=movie_id, review=review, rating=format_rating_score)

    db.session.add(new_review)
    db.session.commit()

    page = request.args.get('page', 1, type=int)
    movies = db.session.query(Movies.Movie).paginate(page=page, per_page=ROWS_PER_PAGE)

    return render_template('index.html', movies=movies, page=page, current_user=current_user)


@main.route("/update_review/", methods=['GET', 'POST'])
def update_review():
    movie_id = request.form['movie_id']
    new_review = request.form['review']
    rating_id = request.form['rating_id']
    user_rating = db.session.query(Rating.Rating).filter(Rating.Rating.id == rating_id).one()

    user_rating.review = new_review
    user_rating.updated_at = datetime.datetime.now()

    db.session.commit()
    return render_template("profile.html")


@main.route("/delete_review/<int:exist_review_id>", methods=['GET', 'POST'])
def delete_review(exist_review_id):
    db.session.query(Rating.Rating).filter(Rating.Rating.id == exist_review_id).delete()
    db.session.commit()

    return render_template("profile.html")


def load_model():
    # Load the saved model
    with open('app/model/model_analyse_sentiment_v2.pkl', 'rb') as file:
        model = pickle.load(file)

    return model
