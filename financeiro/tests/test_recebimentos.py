from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from financeiro.models import Recebimento, Usuario
from financeiro.services.recebimentos import partes_do_recebimento, registrar_recebimento


class RegistrarRecebimentoTests(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username="vagner", password="senha-forte-123", nome="Vagner"
        )

    def test_registra_recebimento_valido(self):
        recebimento = registrar_recebimento(
            usuario=self.usuario,
            cliente="  Confecção Silva  ",
            valor_centavos=48000,
            forma_pagamento="pix",
        )
        self.assertIsNotNone(recebimento.pk)
        self.assertEqual(Recebimento.objects.count(), 1)
        self.assertEqual(recebimento.cliente, "Confecção Silva")
        self.assertEqual(recebimento.valor_centavos, 48000)
        self.assertEqual(recebimento.registrado_por, self.usuario)
        self.assertEqual(recebimento.data, timezone.localdate())

    def test_divisao_de_480_reais_da_240_para_cada_um(self):
        recebimento = registrar_recebimento(
            usuario=self.usuario,
            cliente="Confecção Silva",
            valor_centavos=48000,
            forma_pagamento="dinheiro",
        )
        self.assertEqual(partes_do_recebimento(recebimento), (24000, 24000))

    def test_valor_zero_e_recusado(self):
        with self.assertRaises(ValidationError):
            registrar_recebimento(
                usuario=self.usuario,
                cliente="Confecção Silva",
                valor_centavos=0,
                forma_pagamento="pix",
            )
        self.assertEqual(Recebimento.objects.count(), 0)

    def test_forma_de_pagamento_invalida_e_recusada(self):
        with self.assertRaises(ValidationError):
            registrar_recebimento(
                usuario=self.usuario,
                cliente="Confecção Silva",
                valor_centavos=48000,
                forma_pagamento="cartao",
            )
        self.assertEqual(Recebimento.objects.count(), 0)

    def test_cliente_vazio_e_recusado(self):
        with self.assertRaises(ValidationError):
            registrar_recebimento(
                usuario=self.usuario,
                cliente="   ",
                valor_centavos=48000,
                forma_pagamento="pix",
            )
        self.assertEqual(Recebimento.objects.count(), 0)
