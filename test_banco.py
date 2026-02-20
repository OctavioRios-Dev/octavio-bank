import unittest
from contas import Conta

class TesteBancario(unittest.TestCase):
    def test_deposito(self):
        conta = Conta('Teste', 100)
        conta.depositar(50)
        self.assertEqual(conta.saldo, 150)

    def test_saque_insuficiente(self):
        conta = Conta('Teste', 100)
        resultado = conta.sacar(200)
        self.assertEqual(conta.saldo, 100)

if __name__ == '__main__':
    unittest.main()