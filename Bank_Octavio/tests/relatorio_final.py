import sqlite3

# 1. Conexão
db = sqlite3.connect('bancos_estudos.db')
cursor = db.cursor()

try:
    # 2. Testando o Trigger (O "escudo" para o código não travar)
    print('Tentando inserir saldo negativo...')
    cursor.execute('INSERT INTO contas (saldo, fk_cliente) VALUES (-100, 1)')
    db.commit()
except sqlite3.IntegrityError as e:
    # Ele cai aqui se o Trigger bloquear a inserção
    print(f'✅ Segurança OK! O banco bloqueou: {e}')
except Exception as e:
    # Cai aqui para qualquer outro erro (ex: database is locked)
    print(f'⚠️ Outro erro ocorreu: {e}')

# 3. Relatório Final usando sua VIEW
print('\n--- STATUS FINAL DO BANCOS ---')
try:
    cursor.execute('SELECT * FROM vista_saldos_clientes')
    resultados = cursor.fetchall()

    if not resultados:
        print('Nenhum dado encontrado na VIEW.')
    else:
        for nome, total in resultados:
            print(f'Cliente: {nome} | Saldo Consolidado: R$ {total:.2f}')

except sqlite3.OperationalError as e:
    print(f'❌ Erro: Verifique se a VIEW foi salva no DB Browser! {e}')

db.close()