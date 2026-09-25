import uuid
from typing import List

from pydantic import BaseModel, Field

from app.application.ports import OrderRepository
from app.domain.models import OrderEntity


# =====================================================================
# DTOs (Data Transfer Objects) - Para limpiar la basura que entra de Internet
# =====================================================================
class CreateOrderDTO(BaseModel):
    cliente_id: int = Field(..., gt=0)
    producto: str = Field(..., min_length=3)
    precio: float = Field(..., gt=0.0)
    cantidad: int = Field(..., gt=0)


class OrderResponseDTO(BaseModel):
    """El Presenter: Cómo queremos que el usuario vea la información."""

    id: str
    status: str
    total: float
    mensaje: str


# =====================================================================
# LOS CASOS DE USO (Interactors)
# =====================================================================
class CreateOrderUseCase:
    """Orquesta la creación de una nueva orden."""

    def __init__(self, repo: OrderRepository):
        # Inyección de Dependencias (DIP)
        self.repo = repo

    def ejecutar(self, dto: CreateOrderDTO) -> OrderResponseDTO:
        # 1. Crear ID único y armar la Entidad
        nuevo_id = str(uuid.uuid4())
        orden = OrderEntity(
            id=nuevo_id,
            cliente_id=dto.cliente_id,
            producto=dto.producto,
            precio=dto.precio,
            cantidad=dto.cantidad,
        )

        # 2. Guardar a través del Puerto (No sabemos si es SQL o Memoria)
        self.repo.guardar(orden)

        # 3. Mapear al DTO de Salida
        return OrderResponseDTO(
            id=orden.id,
            status=orden.status.value,
            total=orden.calcular_total(),
            mensaje=f"Orden creada exitosamente para {orden.producto}",
        )


class GetOrdersUseCase:
    """Orquesta la lectura de órdenes."""

    def __init__(self, repo: OrderRepository):
        self.repo = repo

    def ejecutar_todas(self) -> List[OrderEntity]:
        return self.repo.obtener_todas()
