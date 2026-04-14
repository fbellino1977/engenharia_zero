from pydantic import BaseModel, EmailStr, ValidationError

class User(BaseModel):
    id: int
    name: str
    email: EmailStr

if __name__ == "__main__":
    print("--- Teste 1: Dados Corretos ---")
    try:
        user_ok = User(id=1, name="Fabio Bellino", email="br.sp.fb.ti@gmail.com")
        print(f"Sucesso: {user_ok}")
    except ValidationError as e:
        print(f"Erro inesperado: {e}")

    print("\n--- Teste 2: Dados Inválidos (E-mail lixo) ---")
    try:
        user_error = User(id=2, name="Erro", email="isso_nao_e_um_email")
    except ValidationError as e:
        print("Capturado erro de validação como um engenheiro:")
        print(e)