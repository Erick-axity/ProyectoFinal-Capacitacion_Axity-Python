from typing import List

from fastapi import APIRouter, Depends, HTTPException

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

# Creamos el Router de FastAPI
router = APIRouter(prefix="/api/v1/orders", tags=["Orders"])


@router.post("/", response_model=OrderResponseDTO, status_code=201)
def crear_nueva_orden(
    dto: CreateOrderDTO,
    use_case: CreateOrderUseCase = Depends(get_create_order_use_case),
):
    """
    Recibe un DTO validado, se lo avienta al Caso de Uso y devuelve la respuesta.
    El Endpoint no tiene sentencias 'if' ni lógica de negocio.
    """
    try:
        return use_case.ejecutar(dto)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[OrderResponseDTO])
def listar_ordenes(use_case: GetOrdersUseCase = Depends(get_get_orders_use_case)):
    ordenes_entidad = use_case.ejecutar_todas()

    # Mapeamos las Entidades crudas a DTOs formateados para la web
    return [
        OrderResponseDTO(
            id=o.id,
            status=o.status.value,
            total=o.calcular_total(),
            mensaje="Consulta exitosa",
        )
        for o in ordenes_entidad
    ]
