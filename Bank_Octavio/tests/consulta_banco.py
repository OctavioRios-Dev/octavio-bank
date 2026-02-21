import sqlite3

db = sqlite3.connect('bancos_estudos.db')
cursor = db.cursor()

# O comando SELECT é a alma do SQL
cursor.execute('SELECT * FROM clientes')

# Recupera o resultado
clientes = cursor.fetchall()

for cliente in clientes:
    print(f'ID: {cliente[0]} | Nome: {cliente[1]}')

db.close()