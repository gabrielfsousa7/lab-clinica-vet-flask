"""Descrição: Criação das entidades/tabelas da aplicação por meio das classes de modelo e execução das migrations.
Nome do exercício: Aula 17: Modelos e Mapeamento Objeto-Relacional (ORM)
Autor: Gabriel Antônio Ferreira de Sousa
E-mail do aluno: gabriel.sousa12@aluno.cps.sp.gov.br ou gabrielfdesousa2007@gmail.com
Turma: 2 Termo Desenvolvimento de Software 2026 Fatec Olímpia
"""

from flask import Blueprint, request, redirect, url_for, render_template, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_required, login_user, logout_user
from database import db
from models import User

bp = Blueprint("auth", __name__)


@bp.route("/settings")
@login_required
def settings():
    return "Configurações"


@bp.route("/login", methods=("POST", "GET"))
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("ctrl_home.index"))
        flash("Usuário ou senha inválidos")

    return render_template("auth/login.html")


def create_user(password: str):
    user = User(
        username="admin",
        nome="Administrador",
        password=generate_password_hash(password),
        email="admin@admin.com",
    )
    db.session.add(user)
    db.session.commit()
    print(f"Criando usuário {user.as_dict()}")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@bp.route("/change_password", methods=["GET", "POST"])
def change_password():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")
        senha_repetida = request.form.get("senha_repetida")

        if senha_repetida != senha:
            flash("As senhas não conferem")
        else:
            user = User.query.filter_by(email=email).first()
            if user:
                user.password = generate_password_hash(senha_repetida)
                db.session.commit()
                flash("Senha alterada com sucesso")
                return redirect(url_for("auth.login"))
            flash("Usuário não encontrado")

    return render_template("auth/change_password.html")