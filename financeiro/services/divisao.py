"""Regra única da divisão meio a meio (sem Django, só Python)."""


def dividir_meio_a_meio(valor_centavos):
    """Divide um valor em centavos entre duas pessoas.

    Retorna (parte_1, parte_2). Quando o valor tem número ímpar de centavos,
    a sobra de 1 centavo fica SEMPRE com a parte_1. A soma das duas partes é
    sempre igual ao valor recebido.
    """
    if isinstance(valor_centavos, bool) or not isinstance(valor_centavos, int):
        raise ValueError("O valor deve ser um número inteiro de centavos.")
    if valor_centavos <= 0:
        raise ValueError("O valor deve ser maior que zero.")

    parte_2 = valor_centavos // 2
    parte_1 = valor_centavos - parte_2
    return parte_1, parte_2
