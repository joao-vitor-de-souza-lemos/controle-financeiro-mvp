"""Serviços de recebimentos: registro e cálculo da parte de cada um."""
from django.utils import timezone

from financeiro.models import Recebimento

from .divisao import dividir_meio_a_meio


def registrar_recebimento(*, usuario, cliente, valor_centavos, forma_pagamento, data=None):
    """Valida e grava um recebimento feito pelo usuário autenticado.

    Levanta django.core.exceptions.ValidationError se algum dado for inválido.
    """
    recebimento = Recebimento(
        data=data if data is not None else timezone.localdate(),
        cliente=(cliente or "").strip(),
        valor_centavos=valor_centavos,
        forma_pagamento=forma_pagamento,
        registrado_por=usuario,
    )
    recebimento.full_clean()
    recebimento.save()
    return recebimento


def partes_do_recebimento(recebimento):
    """Retorna (parte_1, parte_2) em centavos. A divisão não é gravada no banco."""
    return dividir_meio_a_meio(recebimento.valor_centavos)
