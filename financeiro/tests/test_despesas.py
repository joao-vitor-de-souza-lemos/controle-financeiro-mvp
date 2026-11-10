from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from financeiro.models import Despesa, Usuario
from financeiro.services.despesas import registrar_despesa


class RegistrarDespesaTests(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username="vagner", password="senha-forte-123", nome="Vagner"
        )

    def test_registra_despesa_valida(self):
        despesa = registrar_despesa(
            usuario=self.usuario,
            descricao="  Conta de luz  ",
            categoria="contas_do_local",
            valor_centavos=15000,
        )
        self.assertIsNotNone(despesa.pk)
        self.assertEqual(Despesa.objects.count(), 1)
        self.assertEqual(despesa.descricao, "Conta de luz")
        self.assertEqual(despesa.categoria, "contas_do_local")
        self.assertEqual(despesa.valor_centavos, 15000)
        self.assertEqual(despesa.registrado_por, self.usuario)
        self.assertEqual(despesa.data, timezone.localdate())

    def test_valor_zero_e_recusado(self):
        with self.assertRaises(ValidationError):
            registrar_despesa(
                usuario=self.usuario,
                descricao="Conta de luz",
                categoria="contas_do_local",
                valor_centavos=0,
            )
        self.assertEqual(Despesa.objects.count(), 0)

    def test_categoria_invalida_e_recusada(self):
        with self.assertRaises(ValidationError):
            registrar_despesa(
                usuario=self.usuario,
                descricao="Conta de luz",
                categoria="outra",
                valor_centavos=15000,
            )
        self.assertEqual(Despesa.objects.count(), 0)

    def test_descricao_vazia_e_recusada(self):
        with self.assertRaises(ValidationError):
            registrar_despesa(
                usuario=self.usuario,
                descricao="   ",
                categoria="manutencao",
                valor_centavos=15000,
            )
        self.assertEqual(Despesa.objects.count(), 0)

    def test_data_futura_e_recusada(self):
        amanha = timezone.localdate() + timedelta(days=1)
        with self.assertRaises(ValidationError):
            registrar_despesa(
                usuario=self.usuario,
                descricao="Conserto da máquina",
                categoria="manutencao",
                valor_centavos=15000,
                data=amanha,
            )
        self.assertEqual(Despesa.objects.count(), 0)
