from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "database.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

UPLOAD_FOLDER = os.path.join("static", "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

db = SQLAlchemy(app)


class Empresa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    descricao = db.Column(db.String(200))
    cidade = db.Column(db.String(100))
    endereco = db.Column(db.String(200))
    telefone = db.Column(db.String(20))
    imagem = db.Column(db.String(200))


with app.app_context():
    db.create_all()


@app.route("/", methods=["GET"])
def index():

    busca = request.args.get("busca")

    if busca:
        empresas = Empresa.query.filter(Empresa.nome.contains(busca)).all()
    else:
        empresas = Empresa.query.all()

    return render_template("index.html", empresas=empresas)


@app.route("/add", methods=["GET", "POST"])
def add_empresa():

    if request.method == "POST":

        nome = request.form["nome"]
        descricao = request.form["descricao"]
        cidade = request.form["cidade"]
        endereco = request.form["endereco"]
        telefone = request.form["telefone"]

        imagem_nome = ""

        if "imagem" in request.files:
            file = request.files["imagem"]

            if file.filename != "":
                imagem_nome = file.filename
                caminho = os.path.join(app.config["UPLOAD_FOLDER"], imagem_nome)
                file.save(caminho)

        nova = Empresa(
            nome=nome,
            descricao=descricao,
            cidade=cidade,
            endereco=endereco,
            telefone=telefone,
            imagem=imagem_nome
        )

        db.session.add(nova)
        db.session.commit()

        return redirect("/")

    return render_template("add.html")


@app.route("/deletar/<int:id>")
def deletar(id):

    empresa = Empresa.query.get(id)

    db.session.delete(empresa)
    db.session.commit()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)