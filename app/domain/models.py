from dataclasses import dataclass
from enum import Enum


class StatusOrden(str, Enum):
    PENDIENTE = "pendiente"
    PAGADA = "pagada"
    ENVIADA = "enviada"
    CANCELADA = "cancelada"


@dataclass
class OrderEntity:
    """ENTIDAD: Representa una orden con reglas de negocio estrictas."""

    id: str
    cliente_id: int
    producto: str
    precio: float
    cantidad: int
    status: StatusOrden = StatusOrden.PENDIENTE

    def calcular_total(self) -> float:
        """Cálculo derivado interno de la entidad."""
        return self.precio * self.cantidad

    def pagar(self) -> None:
        """Transición de estado de la entidad."""
        if self.status != StatusOrden.PENDIENTE:
            raise ValueError(
                f"No se puede pagar una orden en estado {self.status.value}"
            )
        self.status = StatusOrden.PAGADA
