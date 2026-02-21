function formatarCores() {
    document.querySelectorAll('.saldo-col').forEach(c => {
        let valorTexto = c.innerText.replace('R$', '').replace(/\./g, '').replace(',', '.').trim();
        let valor = parseFloat(valorTexto);
        c.style.color = valor <= 0 ? '#ff4d4d' : '#4dadff';
    });
}

async function configurarForm(id, rota, msg) {
    const form = document.getElementById(id);
    if (!form) return;
    form.onsubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await fetch(rota, { method: 'POST', body: new FormData(form) });
            const data = await res.json();
            if (data.status === 'sucesso') {
                document.querySelectorAll('tr').forEach(linha => {
                    const tdNome = linha.querySelector('.nome-col');
                    if (tdNome && tdNome.innerText.toUpperCase() === data.nome.toUpperCase()) {
                        linha.querySelector('.saldo-col').innerText = `R$ ${data.novo_saldo.toLocaleString('pt-br', {minimumFractionDigits: 2})}`;
                    }
                });
                formatarCores();
                form.reset();
                alert(msg);
            } else {
                alert('❌ ' + data.mensagem);
            }
        } catch (err) {
            alert('Erro de conexão com o servidor.');
        }
    };
}

window.onload = () => {
    formatarCores();
    configurarForm('form-deposito', '/depositar', '✅ Depósito realizado!');
    configurarForm('form-saque', '/sacar', '💸 Saque realizado!');
};