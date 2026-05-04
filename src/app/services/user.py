from collections.abc import Sequence
from uuid import UUID

from app.core import UserAlreadyExistsError, UserNotFoundError
from app.repositories import UserRepository
from app.schemas import User, UserCreate
from app.security import get_password_hash, verify_password


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def authenticate(self, email: str, password: str) -> User | None:
        try:
            # We try to find the user
            user_model = self.repository.get_by_email(email)

            if not user_model:
                return None

            # If user exists, we verify the password
            if not verify_password(password, user_model.hashed_password):
                return None

            return User.model_validate(user_model)
        except UserNotFoundError:
            # If not found, we return None to avoid user enumeration
            return None

    def get_by_id(self, user_id: int) -> User | None:
        user_model = self.repository.get_by_id(user_id)
        if not user_model:
            raise UserNotFoundError(f"Usuário com ID {user_id} não encontrado")
        return User.model_validate(user_model) if user_model else None

    def get_by_uuid(self, user_uuid_id: UUID) -> User | None:
        user_model = self.repository.get_by_uuid(user_uuid_id)
        if not user_model:
            raise UserNotFoundError(f"Usuário com UUID {user_uuid_id} não encontrado")
        return User.model_validate(user_model) if user_model else None

    def get_by_email(self, email: str) -> User | None:
        user_model = self.repository.get_by_email(email)
        return User.model_validate(user_model) if user_model else None

    def get_all(self, skip: int = 0, limit: int = 10) -> Sequence[User]:
        users_model = self.repository.get_all(skip, limit)
        return [User.model_validate(user_model) for user_model in users_model]

    def create(self, user: UserCreate) -> User:
        # Business Rule Verification: Unique e-mail
        if self.repository.get_by_email(user.email):
            raise UserAlreadyExistsError()

        # Transforms the plaintext password into a secure hash
        # 'user.password' comes from the UserCreate schema
        user.password = get_password_hash(user.password)

        user_model = self.repository.create(user)
        return User.model_validate(user_model)

    def update(self, user_id: int, user: User) -> User | None:
        # We remove field that should not be edited via common profile
        # data_to_update is a dynamic 'dict'
        data_to_update = user.model_dump(
            exclude={"user_id", "user_uuid_id", "is_admin"}
        )

        user_model = self.repository.update(user_id, data_to_update)
        if not user_model:
            raise UserNotFoundError(
                f"Não foi possível atualizar: Usuário {user_id} não existe"
            )

        return User.model_validate(user_model)

    def change_password(self, user_id: int, user_new_password: str) -> None:
        # Generates the new hash and updates the model attribute
        user_new_hashed_password = get_password_hash(user_new_password)

        # This is the place for future validations (e.g., security log)
        self.repository.update_password(user_id, user_new_hashed_password)

    def verify_current_password(self, user_id: int, current_password: str) -> bool:
        # 1. Retrieves the hashed password stored in the database
        hashed_password = self.repository.get_hashed_password(user_id)

        # 2. If there is no hash (user not found or error), it immediately returns False
        if hashed_password is None:
            return False

        # 3. Compares whether the current password matches the one in the database
        return verify_password(current_password, hashed_password)
