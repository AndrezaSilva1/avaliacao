from flask import Flask, flash, redirect, render_template, request, session, url_for

import database
from auth import auth_bp


app = Flask(__name__)
app.secret_key = "chave-secreta"

database.criar_banco()

app.register_blueprint(auth_bp)


@app.route("/")
def index():
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    usuario_id = session["usuario_id"]
    treinos = database.listar_treinos(usuario_id)

    return render_template("index.html", treinos=treinos)


@app.route("/treinos/novo", methods=["GET", "POST"])
def novo_treino():
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        titulo = request.form["titulo"]
        tipo = request.form["tipo"]
        duracao = int(request.form["duracao"])

        usuario_id = session["usuario_id"]

        database.criar_treino(
            titulo,
            tipo,
            duracao,
            usuario_id
        )

        flash("Treino cadastrado.")
        return redirect(url_for("index"))

    return render_template("novo_treino.html")


@app.route("/treinos/<int:treino_id>/editar", methods=["GET", "POST"])
def editar_treino(treino_id):
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    treino = database.buscar_treino(treino_id)

    if treino is None:
        return "Treino não encontrado", 404

    if treino["usuario_id"] != session["usuario_id"]:
        return "Treino não encontrado", 404

    if request.method == "POST":
        titulo = request.form["titulo"]
        tipo = request.form["tipo"]
        duracao = int(request.form["duracao"])

        database.atualizar_treino(
            treino_id,
            titulo,
            tipo,
            duracao
        )

        flash("Treino atualizado.")
        return redirect(url_for("index"))

    return render_template("editar_treino.html", treino=treino)


@app.post("/treinos/<int:treino_id>/concluir")
def concluir_treino(treino_id):
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    treino = database.buscar_treino(treino_id)

    if treino is None:
        return "Treino não encontrado", 404

    if treino["usuario_id"] != session["usuario_id"]:
        return "Treino não encontrado", 404

    database.alternar_concluido(treino_id)

    flash("Status do treino atualizado.")
    return redirect(url_for("index"))


@app.post("/treinos/<int:treino_id>/excluir")
def excluir_treino(treino_id):
    if "usuario_id" not in session:
        return redirect(url_for("auth.login"))

    treino = database.buscar_treino(treino_id)

    if treino is None:
        return "Treino não encontrado", 404

    if treino["usuario_id"] != session["usuario_id"]:
        return "Treino não encontrado", 404

    database.excluir_treino(treino_id)

    flash("Treino excluído.")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)

