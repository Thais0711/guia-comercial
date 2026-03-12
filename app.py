from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Caminho do banco
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "database.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo Loja
class Loja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    telefone = db.Column(db.String(50), nullable=False)
    whatsapp = db.Column(db.String(50), nullable=True)
    premium = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Loja {self.nome}>'

# Criar o banco se não existir
with app.app_context():
    db.create_all()

# Página inicial
@app.route("/")
def index():
    lojas = Loja.query.order_by(Loja.premium.desc(), Loja.nome.asc()).all()
    return render_template("index.html", lojas=lojas)

# Adicionar loja
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        nome = request.form["nome"]
        endereco = request.form["endereco"]
        telefone = request.form["telefone"]
        whatsapp = request.form.get("whatsapp")
        premium = bool(request.form.get("premium"))

        nova_loja = Loja(nome=nome, endereco=endereco, telefone=telefone, whatsapp=whatsapp, premium=premium)
        db.session.add(nova_loja)
        db.session.commit()
        return redirect("/")
    return render_template("add.html")

# Deletar loja
@app.route("/deletar/<int:id>")
def deletar(id):
    loja = Loja.query.get(id)
    if loja:
        db.session.delete(loja)
        db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)