# main.py 

from contas import Conta, Poupança
from colorama import Fore, Style, init

init(autoreset=True)

octavio = Conta('Octavio', 100)
amigo = Conta ('Amigo', 50)

try:
    entrada = input(f'Digite o valor para transferir de {octavio.titular} | Destino: {amigo.titular}\n')
    valor = float(entrada)

    octavio.transferir(valor, amigo)

    with open('Comprovante.txt', 'w', encoding='utf-8') as arquivo:
        arquivo.write(f'=== COMPROVANTE DE TRANSFERENCIA ===\n')
        arquivo.write(f'Origem: {octavio.titular} | Destino: {amigo.titular}\n')
        arquivo.write(f'Valor: R${valor}\n')
        arquivo.write(f'Saldo final Octavio: R${octavio.saldo}\n')

    print(Fore.GREEN + 'Arquivo "comprovante.txt" gerado com sucesso!')
          
except ValueError:
    print(Fore.RED + 'Erro: Voce digitou um valor invalido! Use apenas numeros.')

except Exception as e:
    print(Fore.RED + f'Ocorreu um erro inesperado: {e}')

finally:
    print(Style.BRIGHT + '\n--- Fim da operação bancaria ---')
    print(f'Saldo Octavio: R${octavio.saldo}')
    print(amigo.ver_saldo())