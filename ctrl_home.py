from flask import Blueprint, redirect, url_for, render_template
from flask_login import current_user

bp = Blueprint("ctrl_home", __name__)


@bp.route("/")
def index():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))
    return render_template("index.html")