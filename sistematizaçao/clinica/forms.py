from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
import re
from clinica.models import Usuario
from datetime import datetime

class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Fazer login")


class FormCriarConta(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    username = StringField("Nome de usuário", validators=[DataRequired()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField("Confirme a senha", validators=[DataRequired(), EqualTo("senha")])
    cpf = StringField("CPF", validators=[DataRequired(), Length(11, 11, message="CPF deve conter 11 dígitos")])
    submit = SubmitField("Criar conta") 

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("E-mail ja cadastrado, faça ligin para continuar")


    def validate_cpf(self, cpf):
        """Valida se o CPF contém exatamente 11 números, ignorando pontos e hífens."""
        cpf_limpo = re.sub(r'[^0-9]', '', cpf.data)  # Remove pontos e hífen
        if not re.fullmatch(r"\d{11}", cpf_limpo):  
            raise ValidationError("O CPF deve conter exatamente 11 números.")
        
class FormAgendamento(FlaskForm):
    especialidade = SelectField("Especialidade", validators=[DataRequired()], coerce=int)
    profissional = SelectField("Profissional", validators=[DataRequired()], coerce=int)
    data_hora = DateTimeField("Data e Hora", validators=[DataRequired()], format="%Y-%m-%d %H:%M", default=datetime.now)
    botao_confirmacao = SubmitField("Agendar")
