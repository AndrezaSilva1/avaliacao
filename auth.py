from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

import database


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        if not nome or not email or not senha:
            flash("Preencha todos os campos.")
            return redirect(url_for("auth.registro"))

        usuario = database.buscar_usuario_por_email(email)

        if usuario is not None:
            flash("Este email já está cadastrado.")
            return redirect(url_for("auth.registro"))

        senha_hash = generate_password_hash(senha)

        database.criar_usuario(nome, email, senha_hash)

        flash("Cadastro realizado com sucesso.")
        return redirect(url_for("auth.login"))

    return render_template("registro.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        usuario = database.buscar_usuario_por_email(email)

        if usuario is None or not check_password_hash(usuario.senha_hash, senha):
            flash("Email ou senha inválidos.")
            return redirect(url_for("auth.login"))

        session["usuario_id"] = usuario.id
        session["usuario_nome"] = usuario.nome

        flash("Login realizado com sucesso.")
        return redirect(url_for("index"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.pop("usuario_id", None)
    session.pop("usuario_nome", None)

    flash("Logout realizado com sucesso.")
    return redirect(url_for("auth.login"))