"""Formulários de entrada. A regra de negócio fica nos Services."""
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Despesa, Recebimento
from .services.dinheiro import reais_para_centavos

OBRIGATORIO = {"required": "Preencha este campo."}
ESCOLHA = {
    "required": "Escolha uma das opções.",
    "invalid_choice": "Escolha uma das opções.",
}


class _FormularioLancamento(forms.Form):
    data = forms.DateField(
        label="Data",
        initial=timezone.localdate,
        widget=forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        error_messages={"required": "Informe a data.", "invalid": "Informe uma data válida."},
    )
    valor = forms.CharField(
        label="Valor (R$)",
        max_length=14,
        widget=forms.TextInput(
            attrs={"inputmode": "decimal", "autocomplete": "off", "placeholder": "Ex.: 480,00"}
        ),
        error_messages=OBRIGATORIO,
    )

    def clean_valor(self):
        try:
            return reais_para_centavos(self.cleaned_data["valor"])
        except ValueError:
            raise ValidationError("Informe um valor maior que zero, como 480,00.")


class RecebimentoForm(_FormularioLancamento):
    cliente = forms.CharField(
        label="Cliente",
        max_length=80,
        widget=forms.TextInput(attrs={"autocomplete": "off"}),
        error_messages=OBRIGATORIO,
    )
    forma_pagamento = forms.ChoiceField(
        label="Forma de pagamento",
        choices=Recebimento.FormaPagamento.choices,
        widget=forms.RadioSelect,
        error_messages=ESCOLHA,
    )
    field_order = ["data", "cliente", "valor", "forma_pagamento"]


class DespesaForm(_FormularioLancamento):
    descricao = forms.CharField(
        label="Descrição",
        max_length=100,
        widget=forms.TextInput(attrs={"autocomplete": "off"}),
        error_messages=OBRIGATORIO,
    )
    categoria = forms.ChoiceField(
        label="Categoria",
        choices=Despesa.Categoria.choices,
        widget=forms.RadioSelect,
        error_messages=ESCOLHA,
    )
    field_order = ["data", "descricao", "valor", "categoria"]
