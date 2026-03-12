from app import app, db  # seu app Flask e o db

# cria todas as tabelas dentro do contexto da aplicação
with app.app_context():
    db.create_all()
    print("Banco de dados criado com sucesso!")