# Engenharia Zero API 🚀

Uma API robusta de gestão de faturas desenvolvida com FastAPI, SQLAlchemy e Pydantic. Este projeto demonstra boas práticas de engenharia de software, incluindo transações atômicas, snapshot de preços e testes automatizados.

## 🛠️ Tecnologias Utilizadas

* Python 3.14+
* FastAPI: Framework web moderno e rápido.
* SQLAlchemy 2.0: ORM para mapeamento de banco de dados.
* Pydantic 2: Validação de dados e schemas.
* Alembic: Gestão de migrações de banco de dados.
* Pytest: Suíte de testes automatizados.
* Docker & UV: Containerização e gerenciamento de pacotes ultra-rápido.

## 🚀 Como Executar

### Usando Docker (Recomendado)

1. Certifique-se de ter o Docker instalado.
2. Na raiz do projeto, execute o build: 
   docker build -t engenharia-zero .
3. Execute o container: 
   docker run -p 8000:8000 engenharia-zero
4. Acesse a documentação em: http://localhost:8000/docs

### Desenvolvimento Local (com UV)

1. Instale as dependências: 
   uv sync
2. Rode o servidor (garantindo que o Python encontre o pacote local): 
   PYTHONPATH=. uv run uvicorn main:app --reload

## 🧪 Testes

Para rodar a suíte de testes (unidade e integração), utilize o comando:
PYTHONPATH=. uv run pytest

## 📌 Funcionalidades Principais

* Gestão de Usuários: Cadastro com validação de e-mail único.
* Catálogo de Produtos: Registro de itens com preços dinâmicos.
* Faturamento Inteligente:
    * Preço Congelado (Snapshot): O preço do produto é registrado no item da fatura no momento da venda, garantindo integridade histórica.
    * Rollback Automático: Se um produto da lista não existir, a transação é cancelada por completo.
    * Cálculo Dinâmico: O valor total da fatura é calculado em tempo real através de propriedades do modelo.

## 📁 Estrutura do Projeto

* engenharia_zero/: Código fonte da aplicação (Models, Schemas, DB).
* migrations/: Histórico de alterações do banco de dados (Alembic).
* tests/: Testes automatizados.
* main.py: Ponto de entrada da aplicação e definição das rotas.