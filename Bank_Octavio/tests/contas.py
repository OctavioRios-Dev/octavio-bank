# contas.py

class Conta:
    def __init__(self, titular, saldo_inicial):
        self.titular = titular
        self.__saldo = saldo_inicial

# DEPOSITAR

    @property
    def saldo(self):
        return self.__saldo
    
    def depositar(self, valor):
        if valor > 0:
            self.__saldo += valor
            with open('extrato.txt', 'a') as arquivo:
                arquivo.write(f'Cliente: {self.titular} | Deposito: R${valor}\n')
            print(f'deposito de R${valor} realizado!')

# SACAR

    def sacar(self, valor):
        if valor <= self.__saldo:
            self.__saldo -= valor
            print(f'saque de R${valor} realizado!')
            return True
        else:
            print('Saldo Insuficiente!')
            return False

# TRANSFERIR       

    def transferir(self, valor, conta_destino):
        if valor <= self.__saldo:
            self.__saldo -= valor
            conta_destino.depositar(valor)
            print(f'Transferencia de R${valor} enviada para {conta_destino.titular}!')
        else:
            print('saldo insuficiente para transferir!')


    def ver_saldo(self):
        return f'saldo de {self.titular}: R${self.__saldo}'
    
# POUPANÇA
    
class Poupança(Conta):
    def transferir(self, valor, conta_destino):
        taxa = 2
        valor_total = valor + taxa

        print(f'Tentando transferir R${valor} com taxa de R${taxa}...')
        super().transferir(valor_total, conta_destino)

    def render_juros(self):
        print('Calculando rendimentos...')
    