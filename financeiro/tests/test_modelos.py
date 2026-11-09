from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase
from django.utils import timezone

from financeiro.models import Despesa


class DespesaDataTests(SimpleTestCase):
    def test_data_futura_e_recusada(self):
        amanha = timezone.localdate() + timedelta(days=1)
        despesa = Despesa(data=amanha, descricao="Conta de luz", valor_centavos=15000)
        with self.assertRaises(ValidationError):
            despesa.clean()

    def test_data_de_hoje_e_aceita(self):
        despesa = Despesa(data=timezone.localdate(), descricao="Conta de luz", valor_centavos=15000)
        despesa.clean()
