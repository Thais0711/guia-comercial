from flask import Flask, render_template

app = Flask(__name__)

# Lista de lojas de exemplo
lojas = [
    {"nome": "Loja A", "descricao": "Produtos incríveis", "imagem": "loja1.jpg"},
    {"nome": "Loja B", "descricao": "Ofertas imperdíveis", "imagem": "loja2.jpg"},
    {"nome": "Loja C", "descricao": "Variedade e qualidade", "imagem": "loja3.jpg"}
]

@app.route("/")
def home():
    return render_template("index.html", lojas=lojas)

if __name__ == "__main__":
    app.run(debug=True)