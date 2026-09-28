from typing import List, Optional

from app.application.ports import OrderRepository
from app.application.use_cases import CreateOrderDTO, CreateOrderUseCase
from app.domain.models import OrderEntity


# =====================================================================
# EL MOCK: Un Adaptador Falso para Pruebas Rápidas
# =====================================================================
class FakeOrderRepository(OrderRepository):
    """
    Cumple el contrato del Puerto, pero solo guarda datos en una variable.
    Esto permite probar el Caso de Uso sin encender una base de datos SQL.
    """

    def __init__(self):
        self.db_falsa = {}

    def guardar(self, order: OrderEntity) -> None:
        self.db_falsa[order.id] = order

    def obtener_por_id(self, order_id: str) -> Optional[OrderEntity]:
        return self.db_falsa.get(order_id)

    def obtener_todas(self) -> List[OrderEntity]:
        return list(self.db_falsa.values())


# =====================================================================
# LAS PRUEBAS
# =====================================================================
def test_create_order_use_case():
    """Prueba que el Caso de Uso procese el DTO y genere la Entidad correctamente."""
    # 1. Preparamos el entorno (Inyectamos la base de datos falsa)
    repo_falso = FakeOrderRepository()
    caso_de_uso = CreateOrderUseCase(repo=repo_falso)

    # 2. Creamos los datos de entrada (DTO)
    dto_entrada = CreateOrderDTO(
        cliente_id=99, producto="Silla Gamer", precio=150.0, cantidad=2
    )

    # 3. Ejecutamos
    resultado = caso_de_uso.ejecutar(dto_entrada)

    # 4. Validaciones
    assert resultado.id is not None
    assert resultado.status == "pendiente"
    assert resultado.total == 300.0  # El caso de uso debe invocar el cálculo matemático
    assert "creada exitosamente" in resultado.mensaje

    # Aseguramos que el caso de uso SÍ usó la base de datos para guardar la orden
    assert len(repo_falso.db_falsa) == 1
