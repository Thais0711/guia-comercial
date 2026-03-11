from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lojas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo da Loja
class Loja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    telefone = db.Column(db.String(20), nullable=True)
    descricao = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Loja {self.nome}>'

# Rota para listar lojas
@app.route('/')
@app.route('/lojas')
def listar_lojas():
    lojas = Loja.query.all()
    return render_template('lojas.html', lojas=lojas)

# Rota para cadastrar loja
@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form['nome']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        descricao = request.form['descricao']

        nova_loja = Loja(nome=nome, endereco=endereco, telefone=telefone, descricao=descricao)
        db.session.add(nova_loja)
        db.session.commit()
        return redirect(url_for('listar_lojas'))

    return render_template('cadastrar.html')

if __name__ == '__main__':
    # Cria o banco de dados se não existir
    with app.app_context():
        db.create_all()
    app.run(debug=True)