from engenharia_zero.models import User

from pydantic import ValidationError

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from engenharia_zero.database import UserTable

# 1. Conectar ao banco
engine = create_engine("sqlite:///database.db")

# 2. Abrir uma sessão (uma conversa com o banco)
with Session(engine) as session:
    # Validação dos dados
    try:
        # Valida a entrada de dados antes de persistir no banco de dados
        usuario = User(
            id=0,  # Este dado será criado automaticamente pelo banco de dados
            name="Aline",
            age=39,
            email="aline@exemplo.com",
        )

        # Criar um objeto de banco de dados
        novo_usuario = UserTable(
            name=usuario.name, age=usuario.age, email=usuario.email
        )

        # Adicionar e confirmar (commit)
        session.add(novo_usuario)
        session.commit()
        print("Usuário gravado com sucesso!")

        # 3. Ler o dado de volta
        query = select(UserTable).where(UserTable.email == "aline@exemplo.com")
        usuario_recuperado = session.scalar(query)

        print(
            f"Recuperado do banco: {usuario_recuperado.name}, idade: {usuario_recuperado.age}"
        )
    except ValidationError as e:
        print(f"Erro: {e.json()}")
