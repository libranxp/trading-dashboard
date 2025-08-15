from flask import Blueprint, render_template, request, redirect, session
from auth.user_manager import register_user, validate_login

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if validate_login(username, password):
            session["user"] = username
            return redirect("/")
        return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if register_user(username, password):
            return redirect("/login")
        return render_template("register.html", error="Username already exists")
    return render_template("register.html")

@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")
