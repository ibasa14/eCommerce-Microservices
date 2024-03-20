from passlib.context import CryptContext


class PasswordGenerator:
    @property
    def context(self)->CryptContext:
        return CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def generate_hashed_password(
        self, new_password: str
    ) -> str:
        return self.context.hash(
            new_password
        )

    def validate_password(
        self, password: str, hashed_password: str
    ) -> bool:
        return self.context.verify(
            password, hashed_password
        )


def get_pwd_generator() -> PasswordGenerator:
    return PasswordGenerator()


password_generator: PasswordGenerator = get_pwd_generator()
