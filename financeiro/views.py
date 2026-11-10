"""Views: só recebem a requisição e chamam os Services (sem regra de negócio)."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import DespesaForm, RecebimentoForm
from .services.despesas import registrar_despesa
from .services.dinheiro import centavos_para_reais
from .services.recebimentos import partes_do_recebimento, registrar_recebimento
from .services.resumo import resumo_mensal

MESES = [
    "janeiro", "fevereiro", "março", "abril", "maio", "junho",
    "julho", "agosto", "setembro", "outubro", "novembro", "dezembro",
]

# O Service usa "valor_centavos"; o formulário usa "valor".
CAMPOS_DO_SERVICE = {"valor_centavos": "valor"}


def reais(centavos):
    """Formata centavos como 'R$ 1.234,56'. Valor negativo vira '-R$ 1.234,56'."""
    sinal = "-" if centavos < 0 else ""
    return f"{sinal}R$ {centavos_para_reais(abs(centavos))}"


def _aplicar_erros(form, erro):
    """Leva os erros de validação do Service para junto dos campos do formulário."""
    if hasattr(erro, "error_dict"):
        for campo, mensagens in erro.message_dict.items():
            destino = CAMPOS_DO_SERVICE.get(campo, campo)
            if destino not in form.fields:
                destino = None
            for mensagem in mensagens:
                form.add_error(destino, mensagem)
    else:
        for mensagem in erro.messages:
            form.add_error(None, mensagem)


@login_required
def painel(request):
    hoje = timezone.localdate()
    resumo = resumo_mensal(hoje.year, hoje.month)
    contexto = {
        "mes_nome": f"{MESES[hoje.month - 1]} de {hoje.year}",
        "receitas": reais(resumo.receitas_centavos),
        "despesas": reais(resumo.despesas_centavos),
        "saldo": reais(resumo.saldo_centavos),
        "saldo_negativo": resumo.saldo_centavos < 0,
        "parte_1": reais(resumo.parte_1_centavos),
        "parte_2": reais(resumo.parte_2_centavos),
    }
    return render(request, "financeiro/painel.html", contexto)


@login_required
def recebi(request):
    if request.method == "POST":
        form = RecebimentoForm(request.POST)
        if form.is_valid():
            try:
                recebimento = registrar_recebimento(
                    usuario=request.user,
                    cliente=form.cleaned_data["cliente"],
                    valor_centavos=form.cleaned_data["valor"],
                    forma_pagamento=form.cleaned_data["forma_pagamento"],
                    data=form.cleaned_data["data"],
                )
            except ValidationError as erro:
                _aplicar_erros(form, erro)
            else:
                parte_1, parte_2 = partes_do_recebimento(recebimento)
                messages.success(
                    request,
                    f"Salvo! {reais(recebimento.valor_centavos)} recebidos. "
                    f"Metade de cada um: {reais(parte_1)} e {reais(parte_2)}.",
                )
                return redirect("painel")
    else:
        form = RecebimentoForm()

    contexto = {
        "titulo": "Recebi",
        "ajuda": "Registre o dinheiro que entrou. A metade de cada um aparece ao salvar.",
        "form": form,
        "campos": [form["data"], form["cliente"], form["valor"]],
        "opcoes": form["forma_pagamento"],
    }
    return render(request, "financeiro/lancamento.html", contexto)


@login_required
def gastei(request):
    if request.method == "POST":
        form = DespesaForm(request.POST)
        if form.is_valid():
            try:
                despesa = registrar_despesa(
                    usuario=request.user,
                    descricao=form.cleaned_data["descricao"],
                    categoria=form.cleaned_data["categoria"],
                    valor_centavos=form.cleaned_data["valor"],
                    data=form.cleaned_data["data"],
                )
            except ValidationError as erro:
                _aplicar_erros(form, erro)
            else:
                messages.success(
                    request, f"Salvo! Gasto de {reais(despesa.valor_centavos)} registrado."
                )
                return redirect("painel")
    else:
        form = DespesaForm()

    contexto = {
        "titulo": "Gastei",
        "ajuda": "Registre o dinheiro que saiu do negócio.",
        "form": form,
        "campos": [form["data"], form["descricao"], form["valor"]],
        "opcoes": form["categoria"],
    }
    return render(request, "financeiro/lancamento.html", contexto)
