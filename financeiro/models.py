"""Modelos do MVP: Usuario, Recebimento e Despesa.

Todos os valores em dinheiro são guardados em centavos (inteiros), para
evitar erro de arredondamento. A divisão meio a meio NÃO é gravada: ela é
calculada na camada de Services.
"""
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone


class Usuario(AbstractUser):
    """Pessoa com acesso ao sistema (o dono e o filho).

    Reaproveita os campos do Django: username (nome_usuario), password
    (hash Argon2), is_active (ativo) e date_joined (data_cadastro).
    """

    nome = models.CharField("nome", max_length=150)

    REQUIRED_FIELDS = ["nome"]

    class Meta:
        verbose_name = "usuário"
        verbose_name_plural = "usuários"

    def __str__(self):
        return self.nome or self.username


class Recebimento(models.Model):
    """Dinheiro que entrou no negócio (botão Recebi)."""

    class FormaPagamento(models.TextChoices):
        PIX = "pix", "Pix"
        DINHEIRO = "dinheiro", "Dinheiro"

    data = models.DateField("data", default=timezone.localdate)
    cliente = models.CharField("cliente", max_length=80)
    valor_centavos = models.PositiveIntegerField("valor (em centavos)")
    forma_pagamento = models.CharField(
        "forma de pagamento", max_length=10, choices=FormaPagamento.choices
    )
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="recebimentos",
        verbose_name="registrado por",
    )
    criado_em = models.DateTimeField("criado em", auto_now_add=True)

    class Meta:
        verbose_name = "recebimento"
        verbose_name_plural = "recebimentos"
        ordering = ["-data", "-id"]
        constraints = [
            models.CheckConstraint(
                condition=Q(valor_centavos__gt=0),
                name="recebimento_valor_maior_que_zero",
                violation_error_message="O valor deve ser maior que zero.",
            )
        ]

    def __str__(self):
        return f"{self.data} | {self.cliente} | {self.valor_centavos} centavos"


class Despesa(models.Model):
    """Dinheiro que saiu do negócio (botão Gastei)."""

    class Categoria(models.TextChoices):
        CONTAS_DO_LOCAL = "contas_do_local", "Contas do local"
        MANUTENCAO = "manutencao", "Manutenção"
        IMPREVISTOS = "imprevistos", "Imprevistos"

    data = models.DateField("data", default=timezone.localdate)
    descricao = models.CharField("descrição", max_length=100)
    categoria = models.CharField("categoria", max_length=20, choices=Categoria.choices)
    valor_centavos = models.PositiveIntegerField("valor (em centavos)")
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="despesas",
        verbose_name="registrado por",
    )
    criado_em = models.DateTimeField("criado em", auto_now_add=True)

    class Meta:
        verbose_name = "despesa"
        verbose_name_plural = "despesas"
        ordering = ["-data", "-id"]
        constraints = [
            models.CheckConstraint(
                condition=Q(valor_centavos__gt=0),
                name="despesa_valor_maior_que_zero",
                violation_error_message="O valor deve ser maior que zero.",
            )
        ]

    def clean(self):
        super().clean()
        if self.data and self.data > timezone.localdate():
            raise ValidationError({"data": "A data da despesa não pode ser futura."})

    def __str__(self):
        return f"{self.data} | {self.descricao} | {self.valor_centavos} centavos"
