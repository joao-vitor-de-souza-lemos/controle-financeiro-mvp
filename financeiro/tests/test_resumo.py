from datetime import date

from django.test import TestCase

from financeiro.models import Usuario
from financeiro.services.despesas import registrar_despesa
from financeiro.services.recebimentos import registrar_recebimento
from financeiro.services.resumo import resumo_mensal


class ResumoMensalTests(TestCase):
    """Usa meses do passado (2025 e início de 2026) para que as despesas
    nunca sejam datas futuras, em qualquer dia em que o teste rodar."""

    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username="vagner", password="senha-forte-123", nome="Vagner"
        )

    def _receber(self, data, valor_centavos):
        registrar_recebimento(
            usuario=self.usuario,
            cliente="Cliente",
            valor_centavos=valor_centavos,
            forma_pagamento="pix",
            data=data,
        )

    def _gastar(self, data, valor_centavos):
        registrar_despesa(
            usuario=self.usuario,
            descricao="Gasto",
            categoria="manutencao",
            valor_centavos=valor_centavos,
            data=data,
        )

    def test_soma_so_o_mes_pedido_incluindo_o_primeiro_e_o_ultimo_dia(self):
        self._receber(date(2026, 2, 28), 99999)  # fora (mês anterior)
        self._receber(date(2026, 3, 1), 48000)  # dentro (1º dia)
        self._receber(date(2026, 3, 31), 10001)  # dentro (último dia)
        self._receber(date(2026, 4, 1), 77777)  # fora (mês seguinte)
        self._gastar(date(2026, 2, 28), 5000)  # fora
        self._gastar(date(2026, 3, 15), 15000)  # dentro
        self._gastar(date(2026, 4, 1), 3000)  # fora

        resumo = resumo_mensal(2026, 3)

        self.assertEqual(resumo.receitas_centavos, 58001)
        self.assertEqual(resumo.despesas_centavos, 15000)
        self.assertEqual(resumo.saldo_centavos, 43001)
        self.assertEqual(resumo.parte_1_centavos, 21501)
        self.assertEqual(resumo.parte_2_centavos, 21500)

    def test_mes_sem_lancamentos_retorna_zeros(self):
        resumo = resumo_mensal(2026, 1)
        self.assertEqual(resumo.receitas_centavos, 0)
        self.assertEqual(resumo.despesas_centavos, 0)
        self.assertEqual(resumo.saldo_centavos, 0)
        self.assertEqual(resumo.parte_1_centavos, 0)
        self.assertEqual(resumo.parte_2_centavos, 0)

    def test_saldo_negativo_com_centavo_impar(self):
        self._receber(date(2026, 1, 2), 1000)
        self._gastar(date(2026, 1, 3), 3001)

        resumo = resumo_mensal(2026, 1)

        self.assertEqual(resumo.saldo_centavos, -2001)
        self.assertEqual(resumo.parte_1_centavos, -1001)
        self.assertEqual(resumo.parte_2_centavos, -1000)

    def test_dezembro_nao_inclui_janeiro_do_ano_seguinte(self):
        self._receber(date(2025, 12, 31), 1000)
        self._receber(date(2026, 1, 1), 5000)

        resumo = resumo_mensal(2025, 12)

        self.assertEqual(resumo.receitas_centavos, 1000)

    def test_mes_invalido_e_recusado(self):
        for ano, mes in ((2026, 0), (2026, 13), ("2026", 3)):
            with self.subTest(ano=ano, mes=mes):
                with self.assertRaises(ValueError):
                    resumo_mensal(ano, mes)
