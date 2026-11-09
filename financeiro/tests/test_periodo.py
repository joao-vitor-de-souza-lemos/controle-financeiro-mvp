import unittest
from datetime import date

from financeiro.services.periodo import limites_do_mes


class LimitesDoMesTests(unittest.TestCase):
    def test_mes_comum(self):
        self.assertEqual(limites_do_mes(2026, 3), (date(2026, 3, 1), date(2026, 4, 1)))

    def test_dezembro_vira_janeiro_do_ano_seguinte(self):
        self.assertEqual(limites_do_mes(2025, 12), (date(2025, 12, 1), date(2026, 1, 1)))

    def test_fevereiro_de_ano_bissexto(self):
        self.assertEqual(limites_do_mes(2028, 2), (date(2028, 2, 1), date(2028, 3, 1)))

    def test_valores_invalidos_sao_recusados(self):
        for ano, mes in ((2026, 0), (2026, 13), (1999, 5), (2101, 5), ("2026", 3), (2026, "3"), (2026, True)):
            with self.subTest(ano=ano, mes=mes):
                with self.assertRaises(ValueError):
                    limites_do_mes(ano, mes)
