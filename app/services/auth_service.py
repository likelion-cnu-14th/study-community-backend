from datetime import datetime, timezone

from fastapi import HTTPException

from ..models import User
from ..schemas import UserRegister, UserLogin
from ..repositories import UserRepository
from ..auth import hash_password, verify_password, create_access_token


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register(self, data: UserRegister) -> tuple[User, str]:
        if len(data.username) < 2:
            raise HTTPException(status_code=400, detail="사용자 이름은 2자 이상이어야 합니다.")
        if len(data.password) < 6:
            raise HTTPException(status_code=400, detail="비밀번호는 6자 이상이어야 합니다.")

        if self.user_repo.find_by_email(data.email):
            raise HTTPException(status_code=409, detail="이미 사용 중인 이메일입니다.")
        if self.user_repo.find_by_username(data.username):
            raise HTTPException(status_code=409, detail="이미 사용 중인 사용자 이름입니다.")

        user = User(
            id=str(int(datetime.now(timezone.utc).timestamp() * 1000)),
            username=data.username,
            email=data.email,
            hashed_password=hash_password(data.password),
        )
        user = self.user_repo.save(user)
        token = create_access_token(user.id)
        return user, token

    def login(self, data: UserLogin) -> tuple[User, str]:
        user = self.user_repo.find_by_email(data.email)
        if not user or not verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다.")

        token = create_access_token(user.id)
        return user, token
