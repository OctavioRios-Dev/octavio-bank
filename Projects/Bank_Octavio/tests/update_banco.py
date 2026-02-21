import sqlite3

# 1. Conecta (ou cria) o arquivo do banco
db = sqlite3.connect('bancos_estudos.db')
cursor = db.cursor()

# 2. Criando tabelas seguindo a Normalização (Prática)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS clientes (
               id_cliente INTEGER PRIMARY KEY,
               nome TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS contas (
        id_conta INTEGER PRIMARY KEY,
        saldo REAL,
        fk_cliente INTEGER,
        FOREIGN KEY (fk_cliente) REFERENCES clientes(id_cliente)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS enderecos (
        id_enderecos INTEGER PRIMARY KEY AUTOINCREMENT,
        rua TEXT,
        cidade TEXT,
        fk_cliente INTEGER,
        FOREIGN KEY (fk_cliente) REFERENCES clientes(id_cliente)
    )
''')

# 3. Inserindo dados para testar
cursor.execute('INSERT INTO clientes (nome) VALUES ("Octavio")')
cursor.execute('INSERT INTO contas (saldo, fk_cliente) VALUES (1500.0, 1)')

db.commit()
print('Banco atualizado com a tabela de endereços!')
db.close()