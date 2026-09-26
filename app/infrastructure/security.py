import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# ⬅️ IMPORTAMOS NUESTRAS VARIABLES SEGURAS
from app.infrastructure.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def verificar_token_jwt(token: str = Depends(oauth2_scheme)) -> str:
    try:
        # ⬅️ USAMOS EL SECRETO DESENCRIPTADO DEL .ENV
        payload = jwt.decode(
            token,
            settings.jwt_secret_key.get_secret_value(),
            algorithms=[settings.algorithm],
        )
        username: str = payload.get("sub", "")
        if not username:
            raise ValueError("Token sin 'sub'")
        return username
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado. ¡Acceso Denegado!",
            headers={"WWW-Authenticate": "Bearer"},
        )
