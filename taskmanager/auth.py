from flask import (
    Blueprint,
    render_template,
    request,
    url_for,
    redirect,
    flash,
    session,
    g,
)
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from taskmanager import db

bp = Blueprint("auth", __name__, url_prefix="/auth")
import functools


def login_required(maindef):
    @functools.wraps(maindef)
    def decorator_def(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return maindef(*args, **kwargs)

    return decorator_def
def logued_redirect(maindef):
    @functools.wraps(maindef)
    def decorator_def(*args, **kwargs):
        if g.user:
            return redirect(url_for("taskmanager.index"))
        return maindef(*args, **kwargs)

    return decorator_def


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User(username, generate_password_hash(password))
        error = None
        user_name = User.query.filter_by(username=username).first()
        if user_name == None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        else:
            error = f"El usuario {username} ya esta registrado!"
            flash(error)
    return render_template("auth/register.html")

@bp.route("/login", methods=("GET", "POST"))
@logued_redirect
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User(username, generate_password_hash(password))
        error = None
        user = User.query.filter_by(username=username).first()
        if user == None:
            error = f"El usuario {username} ya esta registrado!"
            flash(error)
        elif not check_password_hash(user.password, password):
            error = f"Contraseña incorrecta"
        if error is None:
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for("taskmanager.index"))
        flash(error)
    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get_or_404(user_id)


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


