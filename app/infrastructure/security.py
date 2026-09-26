import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# SECRET_KEY para encriptar los tokens. En producción esto va en el .env
SECRET_KEY = "FirmaSuperSecretaHexagonal"
ALGORITHM = "HS256"

# Le dice a Swagger (la UI) que busque el botón de Login en esta ruta
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def verificar_token_jwt(token: str = Depends(oauth2_scheme)) -> str:
    """
    Middleware de seguridad.
    Intenta desencriptar el JWT. Si falla o expiró, bloquea la petición.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
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
