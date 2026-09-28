import pytest

from app.domain.models import OrderEntity, StatusOrden


def test_calculo_total_orden():
    """El cálculo matemático debe ser exacto sin importar la tecnología externa."""
    orden = OrderEntity(
        id="123", cliente_id=1, producto="Monitor", precio=250.0, cantidad=4
    )

    # 250.0 * 4 = 1000.0
    assert orden.calcular_total() == 1000.0


def test_cambio_status_exitoso():
    """Una orden pendiente debe poder pasar a estado pagada."""
    orden = OrderEntity(
        id="123", cliente_id=1, producto="Monitor", precio=250.0, cantidad=1
    )

    assert orden.status == StatusOrden.PENDIENTE
    orden.pagar()
    assert orden.status == StatusOrden.PAGADA


def test_cambio_status_invalido():
    """No se debe poder pagar una orden que ya está cancelada."""
    orden = OrderEntity(
        id="123", cliente_id=1, producto="Monitor", precio=250.0, cantidad=1
    )

    orden.status = StatusOrden.CANCELADA

    # Validamos que el sistema "explote" (Falle Rápido) como se espera
    with pytest.raises(
        ValueError, match="No se puede pagar una orden en estado cancelada"
    ):
        orden.pagar()
