from engenharia_zero.models import User
from pydantic import ValidationError

dados_externos = [
    {"id": 1, "name": "Fabio", "age": 48, "email": "fabio@exemplo.com"},
    {"id": "dois", "name": "Erro", "age": 35, "email": "email_ruim"},
    {"id": 3, "name": "Ana", "age": 24, "email": "ana@exemplo.com"},
]

for i, dado in enumerate(dados_externos):
    try:
        # Creates the User
        user = User(**dado)
        print(f"Usuário [{user.name}] criado.")
    except ValidationError as e:
        print(f"Falha no item [{i}]: [{e.json()}]")
