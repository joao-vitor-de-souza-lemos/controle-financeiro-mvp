# Controle Financeiro (MVP)

Aplicação web simples de controle financeiro para uma microempresa familiar de corte de tecido e enfesto em Itaquera, São Paulo. Projeto da disciplina de Projeto de Software (Ciência da Computação, UNICID), ligado ao ODS 8 da ONU (Trabalho Decente e Crescimento Econômico).

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Django](https://img.shields.io/badge/Django-5.2%20LTS-092E20)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-336791)

## Sobre o projeto

A microempresa parceira (Vagner Hermogenes de Souza e o filho, os dois únicos trabalhadores) entrega serviço de corte e enfesto com rapidez, mas não registra nenhuma receita, despesa ou reserva. Os pagamentos chegam por Pix ou dinheiro e são divididos meio a meio sem anotação. Por isso nunca souberam quanto ganham ou gastam por mês, e três imprevistos viraram gastos sem planejamento.

O MVP resolve essa dor com registros em poucos toques, pensados para o celular Android que os dois já usam.

## Funcionalidades do MVP

- Login simples para os dois usuários
- Registro de recebimentos (botão **Recebi**): data, cliente, valor e forma de pagamento (Pix ou dinheiro)
- Registro de despesas (botão **Gastei**): data, descrição, categoria e valor
- Divisão automática meio a meio de cada recebimento
- Painel mensal com receitas, despesas, saldo e parte de cada um
- Histórico de lançamentos com filtro por mês
- Reserva de emergência com meta (funcionalidade desejável)

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.12 |
| Framework web | Django 5.2 LTS (padrão MVT, com camada de Services) |
| Banco de dados | PostgreSQL 17 (Neon) |
| Interface | Templates Django com Bootstrap 5.3, mobile first |
| Segurança | Hash de senha Argon2, proteção CSRF, consultas parametrizadas pelo ORM |
| Publicação | Gunicorn, WhiteNoise e Render |

## Arquitetura

Monolito em camadas: Templates (apresentação), Views (controle), Services (regras de negócio) e Models (persistência). A regra de divisão e o cálculo do saldo ficam em um único ponto, a camada de Services.

## Status

Em desenvolvimento. O planejamento, a arquitetura, os requisitos e o protótipo das telas já foram definidos nas etapas anteriores do projeto. A implementação segue em incrementos: registros com divisão, painel e histórico, e por último a reserva de emergência.

## Autor

**João Vitor de Souza Lemos**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-joaolemos2004-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/joaolemos2004)
[![GitHub](https://img.shields.io/badge/GitHub-joao--vitor--de--souza--lemos-181717?logo=github&logoColor=white)](https://github.com/joao-vitor-de-souza-lemos)
