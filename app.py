from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Caminho do banco de dados
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo da loja
class Loja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200))
    telefone = db.Column(db.String(20))
    whatsapp = db.Column(db.String(20))
    premium = db.Column(db.Boolean, default=False)

# Cria o banco (se não existir)
with app.app_context():
    db.create_all()

# Rota principal
@app.route("/")
def index():
    lojas = Loja.query.order_by(Loja.premium.desc(), Loja.nome.asc()).all()
    return render_template("index.html", lojas=lojas)

# Cadastrar loja
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        nome = request.form['nome']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        whatsapp = request.form['whatsapp']
        premium = 'premium' in request.form
        
        nova_loja = Loja(nome=nome, endereco=endereco, telefone=telefone, whatsapp=whatsapp, premium=premium)
        db.session.add(nova_loja)
        db.session.commit()
        
        return redirect("/")
    
    return render_template("add.html")

# Deletar loja
@app.route("/deletar/<int:id>")
def deletar(id):
    loja = Loja.query.get(id)
    db.session.delete(loja)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)