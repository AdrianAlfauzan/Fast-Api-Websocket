from datetime import datetime, timedelta
from jose import jwt
from app.repositories.auth import AuthRepository
from app.utils.exception import UnauthorizedException
from app.core.constants.auth import JWT_TOKEN_EXPIRE_IN_MIN
from app.core.config import settings
from app.schemas.user_mgt import AuthUser
import logging
from sqlalchemy.orm import joinedload
from app.schemas.user_mgt import UserRegister
import uuid

class AuthService:
    def __init__(self) -> None:
        self.auth_repo = AuthRepository()

    def register_user(self, user_in: UserRegister) -> str:
            if self.auth_repo.is_username_or_email_used(user_in.username, user_in.email):
                raise UnauthorizedException("Username or email already used")

            self.auth_repo.create_user(
                full_name=user_in.full_name,
                username=user_in.username,
                email=user_in.email,
                password=user_in.password
            )

            return "User registered successfully"
        
    def generate_token(self, identifier: str, password: str) -> str:
        user = self.auth_repo.find_by_username_or_email(identifier)
        if user is None or not self.auth_repo.verify_password(password, user.password):
            raise UnauthorizedException("Invalid credentials")

        expire = datetime.utcnow() + timedelta(minutes=JWT_TOKEN_EXPIRE_IN_MIN)
        encode = {
            "id": str(user.id),
            "full_name": user.full_name,
            "exp": expire
        }
        return jwt.encode(encode, settings.jwt_secret, algorithm=settings.jwt_algorithm)

    def get_user_details(self, user_id: uuid.UUID) -> AuthUser:
        try:
            # Panggil find_by_id tanpa .options(joinedload(User.roles))
            user = self.auth_repo.find_by_id(user_id)

            if user is None:
                raise UnauthorizedException("User not found")

            user_data = AuthUser(
                id=user.id,
                full_name=user.full_name,
                username=user.username,
                email=user.email,
                created_at=user.created_at,
                updated_at=user.updated_at,
                dseleted_at=user.deleted_at,
                created_by=user.created_by,
                # roles=[role.name for role in user.roles]  # Dapatkan nama role
            )
            logging.info(f"User details: {user_data}")
            return user_data
        except Exception as e:
            logging.error(f"Error in get_user_details: {e}")
            raise