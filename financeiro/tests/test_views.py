from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from financeiro.models import Despesa, Recebimento, Usuario
from financeiro.services.despesas import registrar_despesa
from financeiro.services.recebimentos import registrar_recebimento


class AcessoTests(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username="vagner", password="senha-forte-123", nome="Vagner"
        )

    def test_paginas_exigem_login(self):
        for nome in ("painel", "recebi", "gastei"):
            with self.subTest(pagina=nome):
                resposta = self.client.get(reverse(nome))
                self.assertEqual(resposta.status_code, 302)
                self.assertIn(reverse("login"), resposta.url)

    def test_login_com_senha_correta_leva_ao_painel(self):
        resposta = self.client.post(
            reverse("login"), {"username": "vagner", "password": "senha-forte-123"}
        )
        self.assertRedirects(resposta, reverse("painel"))

    def test_login_com_senha_errada_mostra_mensagem_generica(self):
        resposta = self.client.post(
            reverse("login"), {"username": "vagner", "password": "errada"}
        )
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Usuário ou senha incorretos")
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_sair_encerra_a_sessao(self):
        self.client.login(username="vagner", password="senha-forte-123")
        resposta = self.client.post(reverse("logout"))
        self.assertRedirects(resposta, reverse("login"))
        self.assertNotIn("_auth_user_id", self.client.session)


class PainelTests(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username="vagner", password="senha-forte-123", nome="Vagner"
        )
        self.client.login(username="vagner", password="senha-forte-123")

    def test_painel_mostra_nome_blocos_e_botoes(self):
        resposta = self.client.get(reverse("painel"))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Olá, Vagner")
        for texto in ("Receitas", "Despesas", "Saldo", "Parte de cada um", "Recebi", "Gastei", "Sair"):
            self.assertContains(resposta, texto)
        self.assertNotContains(resposta, "Saldo negativo")

    def test_painel_mostra_o_controle_de_tamanho_do_texto(self):
        resposta = self.client.get(reverse("painel"))
        self.assertContains(resposta, 'id="texto-mais"')
        self.assertContains(resposta, 'id="texto-menos"')

    def test_painel_soma_os_lancamentos_do_mes_e_divide_o_saldo(self):
        registrar_recebimento(
            usuario=self.usuario, cliente="Cliente", valor_centavos=48000, forma_pagamento="pix"
        )
        registrar_despesa(
            usuario=self.usuario, descricao="Conta de luz",
            categoria="contas_do_local", valor_centavos=15000,
        )
        resposta = self.client.get(reverse("painel"))
        self.assertContains(resposta, "R$ 480,00")
        self.assertContains(resposta, "R$ 150,00")
        self.assertContains(resposta, "R$ 330,00")
        self.assertContains(resposta, "R$ 165,00")

    def test_saldo_negativo_aparece_com_sinal_simbolo_e_texto(self):
        registrar_recebimento(
            usuario=self.usuario, cliente="Cliente", valor_centavos=1000, forma_pagamento="pix"
        )
        registrar_despesa(
            usuario=self.usuario, descricao="Conserto",
            categoria="manutencao", valor_centavos=3000,
        )
        resposta = self.client.get(reverse("painel"))
        self.assertContains(resposta, "Saldo negativo")
        self.assertContains(resposta, "-R$ 20,00")
        self.assertContains(resposta, "-R$ 10,00")
        self.assertContains(resposta, "&#9888;")


class RecebiTests(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username="vagner", password="senha-forte-123", nome="Vagner"
        )
        self.client.login(username="vagner", password="senha-forte-123")

    def _dados(self, **alterados):
        dados = {
            "data": timezone.localdate().isoformat(),
            "cliente": "Confecção Exemplo",
            "valor": "480,00",
            "forma_pagamento": "pix",
        }
        dados.update(alterados)
        return dados

    def test_formulario_vem_com_a_data_de_hoje(self):
        resposta = self.client.get(reverse("recebi"))
        self.assertContains(resposta, timezone.localdate().isoformat())
        self.assertContains(resposta, "Pix")
        self.assertContains(resposta, "Dinheiro")

    def test_campo_valor_mostra_dica_fixa_sobre_a_virgula(self):
        resposta = self.client.get(reverse("recebi"))
        self.assertContains(resposta, "Pode digitar com ou sem vírgula: 480 ou 480,00.")
        self.assertContains(resposta, 'aria-describedby="dica-valor"')

    def test_valor_sem_virgula_e_aceito(self):
        self.client.post(reverse("recebi"), self._dados(valor="480"))
        self.assertEqual(Recebimento.objects.get().valor_centavos, 48000)

    def test_salvar_grava_e_mostra_a_metade_de_cada_um(self):
        resposta = self.client.post(reverse("recebi"), self._dados(), follow=True)
        self.assertEqual(Recebimento.objects.count(), 1)
        recebimento = Recebimento.objects.get()
        self.assertEqual(recebimento.valor_centavos, 48000)
        self.assertEqual(recebimento.registrado_por, self.usuario)
        self.assertContains(
            resposta, "Metade de cada um: R$ 240,00 e R$ 240,00"
        )

    def test_valor_invalido_mostra_erro_junto_ao_campo_e_nao_grava(self):
        for valor in ("0", "abc", ""):
            with self.subTest(valor=valor):
                resposta = self.client.post(reverse("recebi"), self._dados(valor=valor))
                self.assertEqual(resposta.status_code, 200)
                self.assertContains(resposta, 'role="alert"')
        self.assertEqual(Recebimento.objects.count(), 0)

    def test_forma_de_pagamento_obrigatoria(self):
        dados = self._dados()
        del dados["forma_pagamento"]
        resposta = self.client.post(reverse("recebi"), dados)
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Escolha uma das opções.")
        self.assertEqual(Recebimento.objects.count(), 0)


class GasteiTests(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username="vagner", password="senha-forte-123", nome="Vagner"
        )
        self.client.login(username="vagner", password="senha-forte-123")

    def _dados(self, **alterados):
        dados = {
            "data": timezone.localdate().isoformat(),
            "descricao": "Conserto da máquina de corte",
            "valor": "700,00",
            "categoria": "manutencao",
        }
        dados.update(alterados)
        return dados

    def test_formulario_mostra_as_tres_categorias(self):
        resposta = self.client.get(reverse("gastei"))
        for texto in ("Contas do local", "Manutenção", "Imprevistos"):
            self.assertContains(resposta, texto)

    def test_campo_valor_mostra_dica_fixa_sobre_a_virgula(self):
        resposta = self.client.get(reverse("gastei"))
        self.assertContains(resposta, "Pode digitar com ou sem vírgula: 480 ou 480,00.")

    def test_salvar_grava_e_confirma(self):
        resposta = self.client.post(reverse("gastei"), self._dados(), follow=True)
        self.assertEqual(Despesa.objects.count(), 1)
        self.assertEqual(Despesa.objects.get().valor_centavos, 70000)
        self.assertContains(resposta, "Salvo! Gasto de R$ 700,00 registrado.")

    def test_data_futura_mostra_erro_junto_ao_campo(self):
        amanha = (timezone.localdate() + timedelta(days=1)).isoformat()
        resposta = self.client.post(reverse("gastei"), self._dados(data=amanha))
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "A data da despesa não pode ser futura.")
        self.assertEqual(Despesa.objects.count(), 0)
