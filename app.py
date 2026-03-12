from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuração do banco de dados SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo Loja
class Loja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    telefone = db.Column(db.String(50), nullable=False)

# Cria o banco de dados
with app.app_context():
    db.create_all()

# Rota principal
@app.route("/")
def index():
    lojas = Loja.query.all()
    return render_template("index.html", lojas=lojas)

# Rota de cadastro
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        nome = request.form["nome"]
        endereco = request.form["endereco"]
        telefone = request.form["telefone"]
        nova_loja = Loja(nome=nome, endereco=endereco, telefone=telefone)
        db.session.add(nova_loja)
        db.session.commit()
        return redirect("/")
    return render_template("add.html")

# Rota de exclusão
@app.route("/deletar/<int:id>")
def deletar(id):
    loja = Loja.query.get(id)
    if loja:
        db.session.delete(loja)
        db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)