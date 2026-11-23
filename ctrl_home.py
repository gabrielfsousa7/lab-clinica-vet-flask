"""Descrição: Criação das entidades/tabelas da aplicação por meio das classes de modelo e execução das migrations.
Nome do exercício: Aula 17: Modelos e Mapeamento Objeto-Relacional (ORM)
Autor: Gabriel Antônio Ferreira de Sousa
E-mail do aluno: gabriel.sousa12@aluno.cps.sp.gov.br ou gabrielfdesousa2007@gmail.com
Turma: 2 Termo Desenvolvimento de Software 2026 Fatec Olímpia
"""

from flask import Blueprint, redirect, url_for, render_template
from flask_login import current_user

bp = Blueprint("ctrl_home", __name__)


@bp.route("/")
def index():
    if not current_user.is_authenticated:
        return redirect(url_for("auth.login"))
    return render_template("index.html")