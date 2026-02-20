from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'chave_secreta_para_o_banco'

def get_dados_banco():
    db = sqlite3.connect('bancos_estudos.db')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM vista_saldos_clientes')
    dados = cursor.fetchall()
    db.close()
    return dados

# --- LOGIN E LOGOUT ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario_form = request.form.get('usuario')
        senha_form = request.form.get('senha')

        # Conectando ao banco para ver se o usuário existe
        db = sqlite3.connect('bancos_estudos.db')
        cursor = db.cursor()
        cursor.execute('SELECT login FROM usuarios WHERE login = ? AND senha = ?', (usuario_form, senha_form))
        user = cursor.fetchone()
        db.close()

        if user:
            session['usuario_logado'] = user[0]
            flash('Login realizado com sucesso!')
            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha inválidos')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario_logado', None)
    flash('Você saiu do sistema.')
    return redirect(url_for('login'))

# --- PÁGINA PRINCIPAL PROTEGIDA ---
@app.route('/')
def index():
    if 'usuario_logado' not in session:
        return redirect(url_for('login'))
    lista_saldos = get_dados_banco()
    return render_template('index.html', saldos=lista_saldos)

# --- AÇÕES (EXEMPLO DE DEPÓSITO PROTEGIDO) ---
@app.route('/depositar', methods=['POST'])
def depositar():
    if 'usuario_logado' not in session:
        return jsonify({'status': 'erro', 'mensagem': 'Acesso negado'}), 401

    nome = request.form.get('nome_cliente')
    valor = request.form.get('valor_deposito')

    if nome and valor:
        db = sqlite3.connect('bancos_estudos.db')
        cursor = db.cursor()
        cursor.execute('SELECT id_cliente FROM clientes WHERE nome = ?', (nome,))
        cliente = cursor.fetchone()

        if cliente:
            id_do_cara = cliente[0]
            cursor.execute('INSERT INTO contas (saldo, fk_cliente) VALUES (?, ?)', (valor, id_do_cara))
            db.commit()

            cursor.execute('SELECT total_saldo FROM vista_saldos_clientes WHERE nome = ?', (nome,))
            resultado_saldo = cursor.fetchone()
            novo_total = resultado_saldo[0] if resultado_saldo else 0
            db.close()

            return jsonify({
                'status': 'sucesso',
                'nome': nome,
                'novo_saldo': novo_total
            })
        db.close()
    return jsonify({'status': 'erro', 'mensagem': 'Falha no depósito'}), 400

# ... (Manter as outras rotas: cadastrar, excluir e extrato seguindo essa lógica de proteção)

if __name__ == '__main__':
    app.run(debug=True)