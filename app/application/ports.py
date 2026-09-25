from typing import List, Optional, Protocol

from app.domain.models import OrderEntity


class OrderRepository(Protocol):
    """
    PUERTO DE SALIDA (Secondary Port):
    El contrato que cualquier base de datos (SQL, Mongo, Memoria) DEBE cumplir.
    """

    def guardar(self, order: OrderEntity) -> None: ...

    def obtener_por_id(self, order_id: str) -> Optional[OrderEntity]: ...

    def obtener_todas(self) -> List[OrderEntity]: ...
