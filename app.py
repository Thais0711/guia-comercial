from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuração do banco SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'lojas.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de Loja
class Loja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    imagem = db.Column(db.String(300), nullable=True)

    def __repr__(self):
        return f"<Loja {self.nome}>"

# Cria o banco e tabelas
with app.app_context():
    db.create_all()

# Rotas
@app.route('/')
def home():
    lojas = Loja.query.all()
    return render_template('index.html', lojas=lojas)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        endereco = request.form.get('endereco')
        imagem = request.form.get('imagem') or 'https://via.placeholder.com/150'
        if nome and endereco:
            nova_loja = Loja(nome=nome, endereco=endereco, imagem=imagem)
            db.session.add(nova_loja)
            db.session.commit()
        return redirect(url_for('home'))
    return render_template('cadastro.html')

if __name__ == '__main__':
    app.run(debug=True)