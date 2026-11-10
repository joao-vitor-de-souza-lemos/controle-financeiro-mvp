# Controle Financeiro (MVP)

Aplicação web simples de controle financeiro para uma microempresa familiar de corte de tecido e enfesto em Itaquera, São Paulo. Projeto da disciplina de Projeto de Software (Ciência da Computação, UNICID), ligado ao ODS 8 da ONU (Trabalho Decente e Crescimento Econômico).

![CI](https://github.com/joao-vitor-de-souza-lemos/controle-financeiro-mvp/actions/workflows/ci.yml/badge.svg)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Django](https://img.shields.io/badge/Django-5.2%20LTS-092E20)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-336791)

## Sobre o projeto

A microempresa parceira (Vagner Hermogenes de Souza e o filho, os dois únicos trabalhadores) entrega serviço de corte e enfesto com rapidez, mas não registra nenhuma receita, despesa ou reserva. Os pagamentos chegam por Pix ou dinheiro e são divididos meio a meio sem anotação. Por isso nunca souberam quanto ganham ou gastam por mês, e três imprevistos viraram gastos sem planejamento.

O MVP resolve essa dor com registros em poucos toques, pensados para o celular Android que os dois já usam.

## Funcionalidades

Já implementadas:

- Login e saída, com acesso protegido por usuário e senha (hash Argon2, mínimo de 10 caracteres)
- Registro de recebimentos (botão **Recebi**): data, cliente, valor e forma de pagamento (Pix ou dinheiro)
- Registro de despesas (botão **Gastei**): data, descrição, categoria (contas do local, manutenção ou imprevistos) e valor
- Divisão automática meio a meio de cada recebimento, com o centavo ímpar sempre na mesma parte
- Painel mensal com receitas, despesas, saldo e parte de cada um
- Acessibilidade: botões de no mínimo 44 por 44 pixels, texto de no mínimo 16 pixels, ajuste do tamanho do texto (A- e A+), erro junto ao campo e alerta de saldo negativo com sinal, símbolo e texto

Próximos incrementos: histórico de lançamentos com filtro por mês e reserva de emergência com meta (desejável).

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.12 |
| Framework web | Django 5.2 LTS (padrão MVT, com camada de Services) |
| Banco de dados | PostgreSQL 17 (Neon); SQLite no desenvolvimento local |
| Interface | Templates Django com CSS próprio, mobile first |
| Segurança | Hash de senha Argon2, proteção CSRF, consultas parametrizadas pelo ORM |
| Publicação | Gunicorn, WhiteNoise e Render |
| Qualidade | Testes automatizados (unitários e de integração), cobertura com coverage e CI no GitHub Actions |

## Arquitetura

Monolito em camadas: Templates (apresentação), Views (controle), Services (regras de negócio) e Models (persistência). A regra de divisão e o cálculo do saldo ficam em um único ponto, a camada de Services.

## Como executar localmente

```
git clone https://github.com/joao-vitor-de-souza-lemos/controle-financeiro-mvp.git
cd controle-financeiro-mvp
python -m venv .venv
.venv\Scripts\Activate.ps1        # Windows (PowerShell). No Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env            # Linux/macOS: cp .env.example .env
python manage.py migrate
python manage.py createsuperuser  # informe usuário, nome e uma senha com 10 ou mais caracteres
python manage.py runserver
```

Abra http://127.0.0.1:8000/ e entre com o usuário criado.

## Testes e cobertura

```
python manage.py test
coverage run --source=financeiro,config --omit="*/migrations/*,*/tests/*,*/wsgi.py,*/asgi.py" manage.py test
coverage report
```

A cada push, o GitHub Actions instala as dependências, verifica o projeto e roda os testes com cobertura.

## Publicação (Render e Neon)

O sistema é publicado no Render (serviço web gratuito) com o banco PostgreSQL da Neon.

| Item | Valor |
|---|---|
| Build Command | `bash build.sh` |
| Start Command | `python -m gunicorn config.wsgi:application` |
| Python | 3.12 (arquivo `.python-version`) |
| Variáveis de ambiente | `SECRET_KEY`, `DATABASE_URL` e `WEB_CONCURRENCY` |

O `build.sh` instala as dependências, coleta os arquivos estáticos e aplica as migrações a cada publicação. O endereço público é liberado automaticamente pela variável `RENDER_EXTERNAL_HOSTNAME`. Nenhum segredo fica no repositório: o arquivo `.env` está no `.gitignore`.

No plano gratuito, o serviço hiberna após 15 minutos sem acesso e leva cerca de 1 minuto para acordar no primeiro acesso seguinte.

## Status

Em desenvolvimento. O planejamento, a arquitetura, os requisitos e o protótipo das telas foram definidos nas etapas anteriores do projeto. A implementação segue em incrementos: registros com divisão, painel e acessibilidade (concluídos), histórico e, por último, a reserva de emergência.

## Autor

**João Vitor de Souza Lemos**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-joaolemos2004-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/joaolemos2004)
[![GitHub](https://img.shields.io/badge/GitHub-joao--vitor--de--souza--lemos-181717?logo=github&logoColor=white)](https://github.com/joao-vitor-de-souza-lemos)
