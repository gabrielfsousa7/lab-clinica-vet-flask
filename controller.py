"""Descrição: Criação das entidades/tabelas da aplicação por meio das classes de modelo e execução das migrations.
Nome do exercício: Aula 17: Modelos e Mapeamento Objeto-Relacional (ORM)
Autor: Gabriel Antônio Ferreira de Sousa
E-mail do aluno: gabriel.sousa12@aluno.cps.sp.gov.br ou gabrielfdesousa2007@gmail.com
Turma: 2 Termo Desenvolvimento de Software 2026 Fatec Olímpia
"""

from datetime import datetime
from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_required
from database import db
from models import Tutor, Pet, Agendamento

bp = Blueprint("controller", __name__, url_prefix="/clinica")


@bp.route("/pets")
@login_required
def listar_pets():
    pets = Pet.query.all()
    tutores = Tutor.query.all()
    return render_template("pets.html", pets=pets, tutores=tutores)


@bp.route("/pets/novo", methods=["POST"])
@login_required
def criar_pet():
    pet = Pet(
        nome=request.form.get("nome"),
        especie=request.form.get("especie"),
        raca=request.form.get("raca"),
        idade=int(request.form.get("idade")),
        tutor_id=int(request.form.get("tutor_id")),
    )
    db.session.add(pet)
    db.session.commit()
    flash("Pet cadastrado!")
    return redirect(url_for("controller.listar_pets"))


@bp.route("/agendamentos")
@login_required
def listar_agendamentos():
    agendamentos = Agendamento.query.all()
    pets = Pet.query.all()
    return render_template("agendamentos.html", agendamentos=agendamentos, pets=pets)


@bp.route("/agendamentos/novo", methods=["POST"])
@login_required
def criar_agendamento():
    data_hora = datetime.strptime(request.form.get("data_hora"), "%Y-%m-%dT%H:%M")
    ag = Agendamento(
        data_hora=data_hora,
        servico=request.form.get("servico"),
        valor=float(request.form.get("valor")),
        observacoes=request.form.get("observacoes"),
        pet_id=int(request.form.get("pet_id")),
    )
    db.session.add(ag)
    db.session.commit()
    flash("Agendamento criado!")
    return redirect(url_for("controller.listar_agendamentos"))