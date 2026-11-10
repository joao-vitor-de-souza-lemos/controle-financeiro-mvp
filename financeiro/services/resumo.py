"""Resumo mensal: receitas, despesas, saldo e parte de cada um."""
from dataclasses import dataclass

from django.db.models import Sum

from financeiro.models import Despesa, Recebimento

from .divisao import dividir_saldo_meio_a_meio
from .periodo import limites_do_mes


@dataclass(frozen=True)
class ResumoMensal:
    ano: int
    mes: int
    receitas_centavos: int
    despesas_centavos: int
    saldo_centavos: int
    parte_1_centavos: int
    parte_2_centavos: int


def _total_em_centavos(queryset):
    """Soma o valor no banco (aggregate), sem trazer linhas para o Python."""
    return queryset.aggregate(total=Sum("valor_centavos"))["total"] or 0


def resumo_mensal(ano, mes):
    """Calcula o resumo do mês. Levanta ValueError se ano ou mês forem inválidos."""
    inicio, proximo = limites_do_mes(ano, mes)

    receitas = _total_em_centavos(
        Recebimento.objects.filter(data__gte=inicio, data__lt=proximo)
    )
    despesas = _total_em_centavos(
        Despesa.objects.filter(data__gte=inicio, data__lt=proximo)
    )
    saldo = receitas - despesas
    parte_1, parte_2 = dividir_saldo_meio_a_meio(saldo)

    return ResumoMensal(
        ano=ano,
        mes=mes,
        receitas_centavos=receitas,
        despesas_centavos=despesas,
        saldo_centavos=saldo,
        parte_1_centavos=parte_1,
        parte_2_centavos=parte_2,
    )
