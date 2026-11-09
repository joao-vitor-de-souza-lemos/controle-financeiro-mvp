import unittest

from financeiro.services.divisao import dividir_meio_a_meio


class DividirMeioAMeioTests(unittest.TestCase):
    def test_valor_par_divide_igualmente(self):
        # Exemplo da EP II: 480,00 vira 240,00 para cada um.
        self.assertEqual(dividir_meio_a_meio(48000), (24000, 24000))

    def test_valor_impar_da_a_sobra_sempre_a_parte_1(self):
        self.assertEqual(dividir_meio_a_meio(10001), (5001, 5000))

    def test_um_centavo_fica_com_a_parte_1(self):
        self.assertEqual(dividir_meio_a_meio(1), (1, 0))

    def test_soma_das_partes_e_sempre_o_valor_recebido(self):
        for valor in range(1, 2001):
            parte_1, parte_2 = dividir_meio_a_meio(valor)
            self.assertEqual(parte_1 + parte_2, valor)
            self.assertLessEqual(parte_1 - parte_2, 1)
            self.assertGreaterEqual(parte_1 - parte_2, 0)

    def test_zero_e_negativo_sao_recusados(self):
        for invalido in (0, -1, -48000):
            with self.assertRaises(ValueError):
                dividir_meio_a_meio(invalido)

    def test_tipos_invalidos_sao_recusados(self):
        for invalido in (480.5, "48000", None, True):
            with self.assertRaises(ValueError):
                dividir_meio_a_meio(invalido)
