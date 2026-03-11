from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuração do banco de dados SQLite dentro da pasta 'instance'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'lojas.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Cria a pasta instance se não existir
os.makedirs(app.instance_path, exist_ok=True)

db = SQLAlchemy(app)

# Modelo da tabela Lojas
class Loja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    telefone = db.Column(db.String(20), nullable=True)

# Cria o banco de dados automaticamente
with app.app_context():
    db.create_all()

# Rota inicial - lista todas as lojas
@app.route('/')
def listar_lojas():
    lojas = Loja.query.all()
    return render_template('lojas.html', lojas=lojas)

# Rota para adicionar loja
@app.route('/adicionar', methods=['POST'])
def adicionar_loja():
    nome = request.form.get('nome')
    endereco = request.form.get('endereco')
    telefone = request.form.get('telefone')
    if nome and endereco:
        nova_loja = Loja(nome=nome, endereco=endereco, telefone=telefone)
        db.session.add(nova_loja)
        db.session.commit()
    return redirect(url_for('listar_lojas'))

if __name__ == '__main__':
    app.run(debug=True)