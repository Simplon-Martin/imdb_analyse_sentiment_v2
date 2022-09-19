from flask import Blueprint, render_template, request, flash
from app.models import User, Movies, Rating
from app.db import db

main = Blueprint("main", __name__, url_prefix="/")


@main.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route("/profile", methods=['GET', 'POST'])
def index():
    return render_template('profile.html')

