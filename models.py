from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from database import db


class User(db.Model, UserMixin):
    __tablename__ = "auth_user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    events = relationship("AuthEvent", back_populates="user")

    def as_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "nome": self.nome,
            "email": self.email,
        }


class AuthEvent(db.Model):
    __tablename__ = "auth_event"
    id = db.Column(db.Integer, primary_key=True)
    event_type = db.Column(db.String(150), nullable=False)
    event_log = db.Column(db.String, nullable=False)
    event_timestamp = db.Column(db.String(150), nullable=False)
    user_id = db.Column(ForeignKey("auth_user.id"))
    user = relationship("User", back_populates="events")


class Tutor(db.Model):
    __tablename__ = "tutores"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    telefone = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    pets = relationship("Pet", back_populates="tutor", cascade="all, delete-orphan")


class Pet(db.Model):
    __tablename__ = "pets"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    especie = db.Column(db.String(60), nullable=False)
    raca = db.Column(db.String(100), nullable=True)
    idade = db.Column(db.Integer, nullable=False)
    tutor_id = db.Column(db.Integer, ForeignKey("tutores.id"), nullable=False)
    tutor = relationship("Tutor", back_populates="pets")
    agendamentos = relationship("Agendamento", back_populates="pet", cascade="all, delete-orphan")


class Agendamento(db.Model):
    __tablename__ = "agendamentos"
    id = db.Column(db.Integer, primary_key=True)
    data_hora = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    servico = db.Column(db.String(150), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(40), nullable=False, default="Pendente")
    observacoes = db.Column(db.String(400), nullable=True)
    pet_id = db.Column(db.Integer, ForeignKey("pets.id"), nullable=False)
    pet = relationship("Pet", back_populates="agendamentos")