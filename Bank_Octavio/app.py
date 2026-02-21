from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'chave_segredo_octavio'

def get_db():
    # Garante que o Python use o arquivo correto de 32KB
    caminho_db = os.path.join(os.path.dirname(__file__), 'banco_de_dados.db')
    db = sqlite3.connect(caminho_db)
    db.row_factory = sqlite3.Row
    return db

@app.route('/')
def index():
    if 'usuario_logado' not in session:
        return redirect(url_for('login'))
    db = get_db()
    saldos = db.execute('SELECT * FROM vista_saldos_clientes').fetchall()
    db.close()
    return render_template('index.html', saldos=saldos)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')
        db = get_db()
        user = db.execute('SELECT login FROM usuarios WHERE login = ? AND senha = ?', (usuario, senha)).fetchone()
        db.close()
        if user:
            session['usuario_logado'] = user['login']
            return redirect(url_for('index'))
        flash('Usuário ou senha incorretos')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form.get('nome_cliente')
    if nome:
        db = get_db()
        db.execute('INSERT INTO clientes (nome) VALUES (?)', (nome,))
        db.commit()
        db.close()
    return redirect(url_for('index'))

@app.route('/depositar', methods=['POST'])
def depositar():
    nome = request.form.get('nome_cliente')
    valor = request.form.get('valor_operacao')
    db = get_db()
    cliente = db.execute('SELECT id_cliente, nome FROM clientes WHERE UPPER(nome) = UPPER(?)', (nome,)).fetchone()
    
    if cliente:
        # 1. Registra o saldo na tabela contas
        db.execute('INSERT INTO contas (saldo, fk_cliente) VALUES (?, ?)', (valor, cliente['id_cliente']))
        
        # 2. NOVO: Registra no Histórico
        db.execute('INSERT INTO historico (id_usuario, tipo, valor) VALUES (?, ?, ?)', 
                   (cliente['id_cliente'], 'Deposito', valor))
        
        db.commit()
        res = db.execute('SELECT total_saldo FROM vista_saldos_clientes WHERE UPPER(nome) = UPPER(?)', (nome,)).fetchone()
        db.close()
        return jsonify({'status': 'sucesso', 'nome': cliente['nome'], 'novo_saldo': res['total_saldo']})
    
    db.close()
    return jsonify({'status': 'erro', 'mensagem': 'Cliente não encontrado'})

@app.route('/sacar', methods=['POST'])
def sacar():
    db = get_db()
    try:
        nome = request.form.get('nome_cliente')
        valor_operacao = request.form.get('valor_operacao')
        valor_saque = float(valor_operacao)
        
        with db:
            cliente = db.execute('SELECT id_cliente, nome FROM clientes WHERE UPPER(nome) = UPPER(?)', (nome,)).fetchone()
            if not cliente:
                return jsonify({'status': 'erro', 'mensagem': 'Cliente não encontrado'})

            saldo_info = db.execute('SELECT total_saldo FROM vista_saldos_clientes WHERE UPPER(nome) = UPPER(?)', (nome,)).fetchone()
            saldo_atual = saldo_info['total_saldo'] if saldo_info else 0

            if saldo_atual < valor_saque:
                return jsonify({'status': 'erro', 'mensagem': f'Saldo insuficiente'})

            # 1. Registra o saldo negativo na tabela contas
            db.execute('INSERT INTO contas (saldo, fk_cliente) VALUES (?, ?)', (-valor_saque, cliente['id_cliente']))
            
            # 2. NOVO: Registra no Histórico
            db.execute('INSERT INTO historico (id_usuario, tipo, valor) VALUES (?, ?, ?)', 
                       (cliente['id_cliente'], 'Saque', valor_saque))
            
            novo = db.execute('SELECT total_saldo FROM vista_saldos_clientes WHERE UPPER(nome) = UPPER(?)', (nome,)).fetchone()
            return jsonify({'status': 'sucesso', 'nome': cliente['nome'], 'novo_saldo': novo['total_saldo']})
    except Exception as e:
        return jsonify({'status': 'erro', 'mensagem': str(e)})
    finally:
        db.close()

@app.route('/excluir', methods=['POST'])
def excluir():
    nome = request.form.get('nome_cliente')
    db = get_db()
    cliente = db.execute('SELECT id_cliente FROM clientes WHERE UPPER(nome) = UPPER(?)', (nome,)).fetchone()
    if cliente:
        db.execute('DELETE FROM contas WHERE fk_cliente = ?', (cliente['id_cliente'],))
        db.execute('DELETE FROM clientes WHERE id_cliente = ?', (cliente['id_cliente'],))
        db.commit()
    db.close()
    return redirect(url_for('index'))

@app.route('/extrato/<nome>')
def extrato(nome):
    db = get_db()
    # Busca o ID do cliente pelo nome
    cliente = db.execute('SELECT id_cliente FROM clientes WHERE UPPER(nome) = UPPER(?)', (nome,)).fetchone()
    
    if cliente:
        # Busca todas as transações desse cliente na tabela historico
        transacoes = db.execute('SELECT tipo, valor, data FROM historico WHERE id_usuario = ? ORDER BY data DESC', 
                                (cliente['id_cliente'],)).fetchall()
        db.close()
        return render_template('extrato.html', transacoes=transacoes, nome=nome)
    
    db.close()
    return "Cliente não encontrado", 404

if __name__ == '__main__':
    app.run(debug=True)