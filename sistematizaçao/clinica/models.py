from clinica import database, login_Manager
from datetime import datetime
from flask_login import UserMixin
from enum import Enum

@login_Manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

class StatusAgendamento(Enum):
    AGENDADO = "agendado"
    CONCLUIDO = "concluído"
    CANCELADO = "cancelado"

class Usuario(database.Model, UserMixin):
    __tablename__ = "usuarios"
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(100), nullable=False)
    email = database.Column(database.String(150), unique=True, nullable=False)
    senha = database.Column(database.String(200), nullable=False)
    cpf = database.Column(database.String(14), unique=True, nullable=False)
    tipo = database.Column(database.String(10), nullable=False)  # 'paciente' ou 'profissional'
    
    # Relacionamento com Agendamento
    agendamentos = database.relationship('Agendamento', backref='paciente', lazy=True)

class Medico(database.Model):
    __tablename__ = "medicos"
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String(100), nullable=False)
    especialidade = database.Column(database.String(100), nullable=False)
    crm = database.Column(database.String(100), nullable=False, unique=True)

    agendamentos = database.relationship('Agendamento', backref='medico', lazy=True)  # ADICIONAR ESTA LINHA



class Agendamento(database.Model):
    __tablename__ = "agendamentos"
    id = database.Column(database.Integer, primary_key=True)
    data = database.Column(database.DateTime, nullable=False)
    paciente_id = database.Column(database.Integer, database.ForeignKey('usuarios.id'), nullable=False)
    # Alterei a ForeignKey para apontar para 'medico.id'
    profissional_id = database.Column(database.Integer, database.ForeignKey('medicos.id'), nullable=False)
    status = database.Column(database.Enum(StatusAgendamento), default=StatusAgendamento.AGENDADO, nullable=False)

    def __repr__(self):
        return f"<Agendamento {self.id} - {self.data} - {self.status.value}>"

