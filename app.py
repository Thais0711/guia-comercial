from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lojas.db'
db = SQLAlchemy(app)

class Loja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    endereco = db.Column(db.String(200))
    telefone = db.Column(db.String(20))

@app.route('/')
def listar_lojas():
    lojas = Loja.query.all()
    return render_template('lojas.html', lojas=lojas)

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar_loja():
    if request.method == 'POST':
        nome = request.form['nome']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        loja = Loja(nome=nome, endereco=endereco, telefone=telefone)
        db.session.add(loja)
        db.session.commit()
        return redirect('/')
    return render_template('cadastrar.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)