"""Serviços de despesas: registro validado."""
from django.utils import timezone

from financeiro.models import Despesa


def registrar_despesa(*, usuario, descricao, categoria, valor_centavos, data=None):
    """Valida e grava uma despesa feita pelo usuário autenticado.

    Levanta django.core.exceptions.ValidationError se algum dado for inválido
    (descrição vazia, categoria fora das três permitidas, valor zero, data futura).
    """
    despesa = Despesa(
        data=data if data is not None else timezone.localdate(),
        descricao=(descricao or "").strip(),
        categoria=categoria,
        valor_centavos=valor_centavos,
        registrado_por=usuario,
    )
    despesa.full_clean()
    despesa.save()
    return despesa
