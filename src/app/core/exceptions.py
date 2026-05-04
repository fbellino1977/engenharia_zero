class UserAlreadyExistsError(Exception):
    def __init__(self, message: str = "E-mail já cadastrado no sistema") -> None:
        self.message = message
        super().__init__(self.message)


class UserNotFoundError(Exception):
    def __init__(self, message: str = "Usuário não encontrado") -> None:
        self.message = message
        super().__init__(self.message)
