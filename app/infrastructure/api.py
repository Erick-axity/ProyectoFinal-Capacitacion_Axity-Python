from typing import List

import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.application.use_cases import (
    CreateOrderDTO,
    CreateOrderUseCase,
    GetOrdersUseCase,
    OrderResponseDTO,
)
from app.infrastructure.dependencies import (
    get_create_order_use_case,
    get_get_orders_use_case,
)

# ⬅️ IMPORTAMOS NUESTRO ESCUDO DE SEGURIDAD
from app.infrastructure.security import ALGORITHM, SECRET_KEY, verificar_token_jwt

# 1. ROUTER DE AUTENTICACIÓN (Para conseguir la llave)
auth_router = APIRouter(prefix="/api/v1/auth", tags=["Autenticación"])


@auth_router.post("/login")
def login_fake(form_data: OAuth2PasswordRequestForm = Depends()):
    """Simula una base de datos de usuarios. Usuario: admin, Password: 123"""
    if form_data.username == "admin" and form_data.password == "123":
        # Creamos y sellamos el Token JWT
        token_jwt = jwt.encode(
            {"sub": form_data.username}, SECRET_KEY, algorithm=ALGORITHM
        )
        return {"access_token": token_jwt, "token_type": "bearer"}

    raise HTTPException(status_code=400, detail="Credenciales incorrectas")


# 2. ROUTER DE ÓRDENES (Ahora con Candado)
# ⬅️ IMPORTANTE: dependencies=[Depends(verificar_token_jwt)] protege TODO el router
orders_router = APIRouter(
    prefix="/api/v1/orders",
    tags=["Orders"],
    dependencies=[Depends(verificar_token_jwt)],
)


@orders_router.post("/", response_model=OrderResponseDTO, status_code=201)
def crear_nueva_orden(
    dto: CreateOrderDTO,
    use_case: CreateOrderUseCase = Depends(get_create_order_use_case),
):
    try:
        return use_case.ejecutar(dto)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@orders_router.get("/", response_model=List[OrderResponseDTO])
def listar_ordenes(use_case: GetOrdersUseCase = Depends(get_get_orders_use_case)):
    ordenes_entidad = use_case.ejecutar_todas()
    return [
        OrderResponseDTO(
            id=o.id,
            status=o.status.value,
            total=o.calcular_total(),
            mensaje="Consulta exitosa",
        )
        for o in ordenes_entidad
    ]
