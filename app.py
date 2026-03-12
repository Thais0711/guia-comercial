from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de Loja
class Loja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    telefone = db.Column(db.String(50), nullable=False)
    whatsapp = db.Column(db.String(50), nullable=True)
    premium = db.Column(db.Boolean, default=False)  # Campo para destaque/premium

# Cria o banco se não existir
with app.app_context():
    db.create_all()

# Página inicial
@app.route("/")
def index():
    # Empresas premium aparecem primeiro
    lojas = Loja.query.order_by(Loja.premium.desc(), Loja.nome).all()
    return render_template("index.html", lojas=lojas)

# Formulário para adicionar loja
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        nome = request.form['nome']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        whatsapp = request.form['whatsapp']
        premium = True if request.form.get('premium') else False

        nova_loja = Loja(
            nome=nome, endereco=endereco, telefone=telefone,
            whatsapp=whatsapp, premium=premium
        )
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