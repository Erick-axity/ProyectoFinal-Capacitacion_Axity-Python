from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def obtener_token() -> str:
    """Función de apoyo: Simula el Login para conseguir
    la llave antes de las pruebas."""
    respuesta = client.post(
        "/api/v1/auth/login", data={"username": "admin", "password": "123"}
    )
    return respuesta.json()["access_token"]


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_crear_orden_flujo_completo():
    """Prueba la creación de la orden inyectando el Token de Seguridad."""
    token = obtener_token()
    headers = {"Authorization": f"Bearer {token}"}  # ⬅️ Armamos el candado

    payload = {
        "cliente_id": 101,
        "producto": "Laptop Hexagonal",
        "precio": 1500.50,
        "cantidad": 2,
    }

    # ⬅️ Pasamos el Header con el JWT en la petición
    response = client.post("/api/v1/orders/", json=payload, headers=headers)

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["status"] == "pendiente"
    assert data["total"] == 3001.0


def test_listar_ordenes():
    """Prueba la lectura de órdenes inyectando el Token de Seguridad."""
    token = obtener_token()
    headers = {"Authorization": f"Bearer {token}"}

    # ⬅️ Pasamos el Header con el JWT en la petición
    response = client.get("/api/v1/orders/", headers=headers)

    assert response.status_code == 200
    ordenes = response.json()
    assert isinstance(ordenes, list)
    assert len(ordenes) >= 1
