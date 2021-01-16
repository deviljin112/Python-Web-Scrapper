from flask import Blueprint, redirect, url_for, render_template, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = Blueprint("auth", __name__)


@auth.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if "submit" in request.form.get("submit"):
            name = request.form.get("name")
            email = request.form.get("email")
            password = request.form.get("password")
            username = request.form.get("username")

            if name == "" or email == "" or password == "" or username == "":
                flash("Please fill in all the fields!")
                return redirect(url_for("auth.register"))

            check_email = User.query.filter_by(email=email).first()
            check_username = User.query.filter_by(username=username).first()

            if check_email:
                flash("Email address already exists")
                return redirect(url_for("auth.register"))

            if check_username:
                flash("Username already exists")
                return redirect(url_for("auth.register"))

            new_user = User(
                email=email,
                name=name,
                username=username,
                password=generate_password_hash(password, method="sha256"),
            )

            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for("auth.login"))

    elif request.method == "GET":
        return render_template("register.html")


@auth.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if "submit" in request.form.get("submit"):
            username = request.form.get("username")
            password = request.form.get("password")

            if username == "" or password == "":
                flash("Please fill in all the fields!")
                return redirect(url_for("auth.login"))

            user = User.query.filter_by(username=username).first()

            if not user or not check_password_hash(user.password, password):
                flash("Please check your login details and try again.")
                return redirect(url_for("auth.login"))

            login_user(user)
            return redirect(url_for("main.panel"))

    elif request.method == "GET":
        return render_template("login.html")


@auth.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.home"))