from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, login_user, logout_user, current_user
from clinica import app, database, bcrypt
from clinica.forms import FormLogin, FormCriarConta, FormAgendamento
from clinica.models import Usuario, Agendamento, Medico, StatusAgendamento
from datetime import datetime

# Página inicial com login
@app.route("/", methods=["GET", "POST"])
def homepage():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil"))
        else:
            flash("E-mail ou senha incorretos", "danger")
    return render_template("homepage.html", form=form_login)

# Página de criação de conta
@app.route("/criarconta", methods=["GET", "POST"])
def criarconta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit():
        senha_criptografada = bcrypt.generate_password_hash(form_criarconta.senha.data).decode('utf-8')
        usuario = Usuario(
            nome=form_criarconta.username.data,
            senha=senha_criptografada,
            email=form_criarconta.email.data,
            cpf=form_criarconta.cpf.data,
            tipo="paciente"
        )
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        return redirect(url_for("perfil"))
    return render_template("criarconta.html", form=form_criarconta)

# Página de perfil
@app.route("/perfil", methods=["GET", "POST"])
@login_required
def perfil():
    medicos = Medico.query.all()
    especialidades = list(set([m.especialidade for m in medicos]))
    return render_template("perfil.html", usuario=current_user, medicos=medicos, especialidades=especialidades)

# Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))

# Criar agendamento
@app.route("/criar_agendamento", methods=["POST"])
@login_required
def criar_agendamento():
    data = request.form["data"]
    medico_id = request.form["medico_id"]

    try:
        data_convertida = datetime.fromisoformat(data)
    except ValueError:
        flash("Data inválida.", "danger")
        return redirect(url_for("perfil"))

    agendamento = Agendamento(
        data=data_convertida,
        paciente_id=current_user.id,
        profissional_id=medico_id,
        status=StatusAgendamento.AGENDADO
    )

    database.session.add(agendamento)
    database.session.commit()
    flash("Agendamento criado com sucesso!", "success")
    return redirect(url_for("perfil"))

# Buscar agendamentos por CPF (somente os futuros e agendados)
@app.route("/buscar_agendamentos", methods=["POST"])
@login_required
def buscar_agendamentos():
    cpf = request.form.get("cpf")
    usuario = Usuario.query.filter_by(cpf=cpf).first()

    if not usuario:
        flash("Usuário com esse CPF não foi encontrado.", "danger")
        return redirect(url_for("perfil"))

    agendamentos = Agendamento.query.filter(
        Agendamento.paciente_id == usuario.id,
        Agendamento.data >= datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
        Agendamento.status == StatusAgendamento.AGENDADO
    ).all()

    return render_template(
        "resultado_busca.html",
        usuario=usuario,
        agendamentos=agendamentos,
        StatusAgendamento=StatusAgendamento
    )

# Cancelar agendamento
@app.route("/cancelar_agendamento/<int:id>", methods=["POST"])
@login_required
def cancelar_agendamento(id):
    agendamento = Agendamento.query.get_or_404(id)

    if agendamento.paciente_id != current_user.id:
        flash("Você não tem permissão para cancelar este agendamento.", "danger")
        return redirect(url_for("perfil"))

    agendamento.status = StatusAgendamento.CANCELADO
    database.session.commit()
    flash("Agendamento cancelado com sucesso!", "success")
    return redirect(url_for("perfil"))
