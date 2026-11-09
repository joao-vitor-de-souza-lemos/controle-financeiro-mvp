import unittest

from financeiro.services.dinheiro import centavos_para_reais, reais_para_centavos


class ReaisParaCentavosTests(unittest.TestCase):
    def test_formatos_validos(self):
        casos = {
            "480": 48000,
            "480,00": 48000,
            "12,5": 1250,
            "0,01": 1,
            "1.250,50": 125050,
            "1.250": 125000,
            "R$ 15,90": 1590,
            "  7,05  ": 705,
        }
        for texto, esperado in casos.items():
            with self.subTest(texto=texto):
                self.assertEqual(reais_para_centavos(texto), esperado)

    def test_formatos_invalidos(self):
        for texto in ("", "   ", "abc", "12,345", "12.5", "1.2500,00", "-5", "1,250.50", None, 10):
            with self.subTest(texto=texto):
                with self.assertRaises(ValueError):
                    reais_para_centavos(texto)

    def test_zero_e_recusado(self):
        for texto in ("0", "0,00"):
            with self.subTest(texto=texto):
                with self.assertRaises(ValueError):
                    reais_para_centavos(texto)


class CentavosParaReaisTests(unittest.TestCase):
    def test_formatacao(self):
        casos = {
            0: "0,00",
            5: "0,05",
            48000: "480,00",
            123456: "1.234,56",
            100000000: "1.000.000,00",
            -500: "-5,00",
            -5: "-0,05",
        }
        for centavos, esperado in casos.items():
            with self.subTest(centavos=centavos):
                self.assertEqual(centavos_para_reais(centavos), esperado)

    def test_ida_e_volta(self):
        for centavos in (1, 99, 100, 48000, 125050, 999999):
            self.assertEqual(reais_para_centavos(centavos_para_reais(centavos)), centavos)
