from flask import Flask, render_template, request, redirect

app = Flask(__name__)

lojas = [
    {
        "id":1,
        "nome": "Burger Top",
        "descricao": "Hambúrguer artesanal delicioso",
        "categoria": "Restaurante",
        "imagem": "burger.jpg",
        "whatsapp": "61999999999"
    },
    {
        "id":2,
        "nome": "Salão Beleza Pura",
        "descricao": "Cortes modernos e manicure",
        "categoria": "Salão",
        "imagem": "salao.jpg",
        "whatsapp": "61988888888"
    }
]

@app.route("/")
def home():

    busca = request.args.get("busca")

    if busca:
        resultado = []
        for loja in lojas:
            if busca.lower() in loja["nome"].lower():
                resultado.append(loja)
        return render_template("index.html", lojas=resultado)

    return render_template("index.html", lojas=lojas)


@app.route("/loja/<int:id>")
def loja(id):

    for loja in lojas:
        if loja["id"] == id:
            return render_template("loja.html", loja=loja)


@app.route("/cadastro", methods=["GET","POST"])
def cadastro():

    if request.method == "POST":

        nova_loja = {
            "id": len(lojas) + 1,
            "nome": request.form["nome"],
            "descricao": request.form["descricao"],
            "categoria": request.form["categoria"],
            "imagem": "burger.jpg",
            "whatsapp": request.form["whatsapp"]
        }

        lojas.append(nova_loja)

        return redirect("/")

    return render_template("cadastro.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)