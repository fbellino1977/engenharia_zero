from engenharia_zero.models import User
from pydantic import ValidationError

dados_externos = [
    {"id": 1, "name": "Fabio", "email": "fabio@exemplo.com"},
    {"id": "dois", "name": "Erro", "email": "email_ruim"},
    {"id": 3, "name": "Ana", "email": "ana@exemplo.com"}
]

for i, dado in enumerate(dados_externos):
    try:
        # Cria o usuário
        user = User(**dado)
        print(f"Usuário [{user.name}] criado.")
    except ValidationError as e:
        print(f"Falha no item [{i}]: [{e.json()}]")
    