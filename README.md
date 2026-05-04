# Engenharia do Zero - Backend 🚀

Este projeto é uma API de alta fidelidade técnica desenvolvida com **FastAPI**. O objetivo central é demonstrar a aplicação rigorosa de práticas de Engenharia de Software, com foco em tipagem estática, segurança e arquitetura desacoplada.

## 🛠️ Stack de Engenharia

* **Python 3.13**: Utilizando as últimas features da linguagem.
* **uv**: Gerenciamento de pacotes e ambiente virtual ultra-rápido.
* **FastAPI**: Framework web de alta performance.
* **SQLAlchemy 2.0**: ORM moderno com suporte a tipagem.
* **Pydantic 2**: Schemas e validação de dados rigorosa.

## 🛡️ Pilares de Qualidade (XP)

O projeto adota uma política de **"Verdadeiro ou Nada"** para o pipeline de código:

1. **Linting & Estilo**: `Ruff` para garantir um código limpo e padronizado.
2. **Tipagem Estática**: `Mypy` em modo **Strict** (zero tolerância a tipos implícitos).
3. **Segurança**: `Bandit` para análise de vulnerabilidades em tempo de design.
4. **Testes**: `Pytest` para garantir que o domínio se comporta como esperado.

## 🚀 Como Executar

### Desenvolvimento Local

1. Instale as dependências:
   ```bash
   uv sync

2. Execute o servidor em modo de desenvolvimento:
   ```bash
   uv run fastapi dev src/app/api/main.py

3. Acesse a documentação interativa: http://localhost:8000/docs

## 🧪 Verificação de Integridade

Antes de cada commit, é mandatório que o código passe pelo crivo das ferramentas:

   ```bash
   # Formatação e Lint
   uv run ruff check . --fix && uv run ruff format .

   # Tipagem (Blindagem)
   uv run mypy src

   # Segurança
   uv run bandit -r src/

   # Testes
   uv run pytest

## 📁 Estrutura de Domínios (Arquitetura)

O projeto segue um padrão de separação de responsabilidades:
• src/app/repositories/: Camada de persistência (SQLAlchemy).
• src/app/services/: Lógica de negócio e orquestração.
• src/app/schemas/: Contratos de entrada e saída (Pydantic).
• src/app/api/: Rotas e controladores da API.