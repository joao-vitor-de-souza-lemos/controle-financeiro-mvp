"""Cálculo de períodos (sem Django, só Python)."""
from datetime import date


def limites_do_mes(ano, mes):
    """Retorna (inicio, proximo): o 1º dia do mês e o 1º dia do mês seguinte.

    Serve para filtrar por intervalo (data >= inicio e data < proximo).
    Levanta ValueError se ano ou mês forem inválidos.
    """
    for valor in (ano, mes):
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise ValueError("Ano e mês devem ser números inteiros.")
    if not 1 <= mes <= 12:
        raise ValueError("O mês deve estar entre 1 e 12.")
    if not 2000 <= ano <= 2100:
        raise ValueError("O ano deve estar entre 2000 e 2100.")

    inicio = date(ano, mes, 1)
    proximo = date(ano + 1, 1, 1) if mes == 12 else date(ano, mes + 1, 1)
    return inicio, proximo
