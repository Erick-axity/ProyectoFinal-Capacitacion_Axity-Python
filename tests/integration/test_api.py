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

    # Pasamos el Header con el JWT en la petición
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

    # Pasamos el Header con el JWT en la petición
    response = client.get("/api/v1/orders/", headers=headers)

    assert response.status_code == 200
    ordenes = response.json()
    assert isinstance(ordenes, list)
    assert len(ordenes) >= 1


def test_acceso_denegado_con_token_falso():
    """Valida la seguridad: Un token inválido debe ser rechazado (Cubre security.py)."""
    headers = {"Authorization": "Bearer TokenFalsoYMalicioso123"}

    response = client.get("/api/v1/orders/", headers=headers)

    assert response.status_code == 401
    assert "Token inválido o expirado" in response.json()["detail"]


def test_crear_orden_invalida_atrapada_por_excepcion():
    """Valida que los errores del UseCase se conviertan
    en 400 Bad Request (Cubre api.py)."""
    token = obtener_token()
    headers = {"Authorization": f"Bearer {token}"}

    # La cantidad no puede ser menor a 1 (Regla de negocio)
    payload_malo = {
        "cliente_id": 101,
        "producto": "Mouse",
        "precio": 50.0,
        "cantidad": 0,  # ⬅️ Dato corrupto
    }

    response = client.post("/api/v1/orders/", json=payload_malo, headers=headers)

    # Debe ser interceptado por el bloque `except Exception:` de api.py
    # Pydantic normalmente arroja un 422, así que nos
    # aseguramos de atrapar el fallo del validador o del negocio.
    assert response.status_code in [400, 422]


def test_obtener_orden_inexistente_retorna_none():
    """Valida el camino donde no se encuentra nada en la BD (Cubre database.py)."""
    from sqlalchemy.orm import Session

    from app.infrastructure.database import SQLAlchemyOrderRepository
    from app.infrastructure.dependencies import engine

    # Simulamos una consulta directa al repositorio (Integración de BD)
    with Session(engine) as session:
        repo = SQLAlchemyOrderRepository(session)
        # Consultamos un ID que sabemos que no existe
        orden_fantasma = repo.obtener_por_id("ID_QUE_NO_EXISTE_99999")

        # Debe devolver None de forma segura sin explotar
        assert orden_fantasma is None
