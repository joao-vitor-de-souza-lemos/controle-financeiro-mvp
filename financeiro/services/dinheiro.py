"""Conversão entre texto em reais e centavos (sem Django, só Python)."""
import re

# Aceita "480", "480,5", "480,50", "1.250,50" e "R$ 15,90".
# O ponto só é aceito como separador de milhar (grupos de 3 dígitos).
_PADRAO_REAIS = re.compile(r"^(\d{1,3}(\.\d{3})+|\d+)(,\d{1,2})?$")


def reais_para_centavos(texto):
    """Converte um valor digitado em reais para centavos (inteiro positivo).

    Levanta ValueError se o texto for inválido ou se o valor não for maior que zero.
    """
    if not isinstance(texto, str):
        raise ValueError("Informe o valor em reais.")

    limpo = re.sub(r"R\$|\s", "", texto)
    if not limpo:
        raise ValueError("Informe o valor em reais.")
    if not _PADRAO_REAIS.match(limpo):
        raise ValueError("Valor inválido. Use o formato 1.250,50.")

    parte_inteira, _, parte_decimal = limpo.partition(",")
    reais = int(parte_inteira.replace(".", ""))
    centavos = int(parte_decimal.ljust(2, "0")) if parte_decimal else 0
    total = reais * 100 + centavos

    if total <= 0:
        raise ValueError("O valor deve ser maior que zero.")
    return total


def centavos_para_reais(centavos):
    """Formata centavos como texto em reais, com duas casas (ex.: 123456 -> '1.234,56')."""
    sinal = "-" if centavos < 0 else ""
    reais, resto = divmod(abs(centavos), 100)
    milhares = f"{reais:,}".replace(",", ".")
    return f"{sinal}{milhares},{resto:02d}"
