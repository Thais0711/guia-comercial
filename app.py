from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lojas.db'  # Banco SQLite local
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo da Loja
class Loja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    telefone = db.Column(db.String(20), nullable=True)

# Criar banco de dados
with app.app_context():
    db.create_all()

# Rotas
@app.route('/')
def index():
    lojas = Loja.query.all()
    return render_template('lojas.html', lojas=lojas)

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar_loja():
    if request.method == 'POST':
        nome = request.form['nome']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        nova_loja = Loja(nome=nome, endereco=endereco, telefone=telefone)
        db.session.add(nova_loja)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('cadastrar_loja.html')

if __name__ == '__main__':
    app.run(debug=True)