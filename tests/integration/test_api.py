from fastapi.testclient import TestClient

from app.main import app

# Cliente de pruebas en memoria (No requiere puertos de red)
client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_crear_orden_flujo_completo():
    """
    Simula a un cliente de internet haciendo una petición POST.
    Esto atravesará el Adapter (API) -> UseCase -> Puerto -> SQLite
    """
    payload = {
        "cliente_id": 101,
        "producto": "Laptop Hexagonal",
        "precio": 1500.50,
        "cantidad": 2,
    }

    response = client.post("/api/v1/orders/", json=payload)

    assert response.status_code == 201
    data = response.json()

    # Validamos que el Presenter (DTO de respuesta) hizo su trabajo
    assert "id" in data
    assert data["status"] == "pendiente"
    # Validamos que la Entidad calculó el total: 1500.50 * 2 = 3001.0
    assert data["total"] == 3001.0
    assert "creada exitosamente" in data["mensaje"]


def test_listar_ordenes():
    """Valida que podamos recuperar las órdenes guardadas en la base de datos."""
    response = client.get("/api/v1/orders/")

    assert response.status_code == 200
    ordenes = response.json()

    assert isinstance(ordenes, list)
    assert len(ordenes) >= 1  # Al menos debe estar la que creamos en el test anterior
