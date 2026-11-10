"""Regra única da divisão meio a meio (sem Django, só Python)."""


def _validar_inteiro(valor):
    if isinstance(valor, bool) or not isinstance(valor, int):
        raise ValueError("O valor deve ser um número inteiro de centavos.")


def dividir_meio_a_meio(valor_centavos):
    """Divide um valor em centavos entre duas pessoas.

    Retorna (parte_1, parte_2). Quando o valor tem número ímpar de centavos,
    a sobra de 1 centavo fica SEMPRE com a parte_1. A soma das duas partes é
    sempre igual ao valor recebido.
    """
    _validar_inteiro(valor_centavos)
    if valor_centavos <= 0:
        raise ValueError("O valor deve ser maior que zero.")

    parte_2 = valor_centavos // 2
    parte_1 = valor_centavos - parte_2
    return parte_1, parte_2


def dividir_saldo_meio_a_meio(saldo_centavos):
    """Divide um saldo (positivo, zero ou negativo) entre duas pessoas.

    Reaproveita a regra de dividir_meio_a_meio. Em saldo negativo, a parte_1
    também fica com o centavo ímpar, agora como prejuízo maior
    (ex.: -5 centavos vira (-3, -2)). A soma das partes é sempre o saldo.
    """
    _validar_inteiro(saldo_centavos)
    if saldo_centavos == 0:
        return 0, 0
    if saldo_centavos > 0:
        return dividir_meio_a_meio(saldo_centavos)

    parte_1, parte_2 = dividir_meio_a_meio(-saldo_centavos)
    return -parte_1, -parte_2
