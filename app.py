from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Loja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    query = request.args.get("search")
    if query:
        lojas = Loja.query.filter(
            (Loja.nome.ilike(f"%{query}%")) |
            (Loja.endereco.ilike(f"%{query}%"))
        ).all()
    else:
        lojas = Loja.query.all()
    return render_template("index.html", lojas=lojas, query=query)

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

@app.route("/deletar/<int:id>")
def deletar(id):
    loja = Loja.query.get(id)
    db.session.delete(loja)
    db.session.commit()
    return redirect("/")

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    loja = Loja.query.get(id)
    if request.method == "POST":
        loja.nome = request.form["nome"]
        loja.endereco = request.form["endereco"]
        loja.telefone = request.form["telefone"]
        db.session.commit()
        return redirect("/")
    return render_template("edit.html", loja=loja)

if __name__ == "__main__":
    app.run(debug=True)