import sqlite3

db_path = "database.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Adiciona a coluna whatsapp, se não existir
try:
    cursor.execute("ALTER TABLE loja ADD COLUMN whatsapp TEXT;")
    print("Coluna 'whatsapp' adicionada com sucesso!")
except sqlite3.OperationalError as e:
    print(f"A coluna já existe ou outro erro: {e}")

conn.commit()
conn.close()