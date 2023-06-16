from flask import Blueprint,render_template, request, url_for,redirect,g
from .auth import login_required

from .models import Task, User
from . import db

bp = Blueprint("taskmanager",__name__, url_prefix="/taskmanager")

@bp.route("/list")
@login_required
def index():
    tasks = Task.query.all()
    return render_template("taskmanager/index.html",tasks = tasks)


@bp.route("/create", methods=("GET","POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        task = Task(created_by=g.user.id, title= title, description=desc)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for("taskmanager.index"))
    return render_template("taskmanager/create.html")

def getTask(id):
    task = Task.query.get_or_404(id)
    return task

@login_required
@bp.route("/edit/<int:id>", methods=("GET","POST"))
def edit(id):
    task = getTask(id)
    if request.method == "POST":
        task.title = request.form["title"]
        task.description = request.form["desc"]
        db.session.commit()
        return redirect(url_for("taskmanager.index"))
    return render_template("taskmanager/edit.html", task = task)

@login_required
@bp.route("/delete/<int:id>", methods=("GET","POST"))
def delete(id):
    task = getTask(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("taskmanager.index"))
    