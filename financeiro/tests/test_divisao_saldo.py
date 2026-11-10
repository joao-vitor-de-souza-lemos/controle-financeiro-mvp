import unittest

from financeiro.services.divisao import dividir_saldo_meio_a_meio


class DividirSaldoMeioAMeioTests(unittest.TestCase):
    def test_saldo_zero(self):
        self.assertEqual(dividir_saldo_meio_a_meio(0), (0, 0))

    def test_saldo_positivo_segue_a_regra_do_centavo_impar(self):
        self.assertEqual(dividir_saldo_meio_a_meio(48000), (24000, 24000))
        self.assertEqual(dividir_saldo_meio_a_meio(43001), (21501, 21500))

    def test_saldo_negativo_espelha_a_regra(self):
        self.assertEqual(dividir_saldo_meio_a_meio(-48000), (-24000, -24000))
        self.assertEqual(dividir_saldo_meio_a_meio(-5), (-3, -2))

    def test_soma_das_partes_e_sempre_o_saldo(self):
        for saldo in range(-500, 501):
            parte_1, parte_2 = dividir_saldo_meio_a_meio(saldo)
            self.assertEqual(parte_1 + parte_2, saldo)

    def test_tipos_invalidos_sao_recusados(self):
        for invalido in (10.5, "10", None, True):
            with self.assertRaises(ValueError):
                dividir_saldo_meio_a_meio(invalido)
