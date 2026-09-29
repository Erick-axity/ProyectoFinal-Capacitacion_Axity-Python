import uuid  # ⬅️ IMPORTANTE: Traemos el generador de IDs únicos

from sqlalchemy.orm import Session

from app.domain.models import OrderEntity
from app.infrastructure.database import SQLAlchemyOrderRepository
from app.infrastructure.dependencies import engine


def test_contrato_repositorio_sql():
    """
    Prueba de Contrato: Valida que el adaptador
    SQL respete los métodos del Puerto
    y sea capaz de guardar y recuperar
    entidades puras de dominio.
    """
    # Generamos un ID dinámico para que
    # el test pueda correr infinitas veces sin chocar
    id_dinamico = str(uuid.uuid4())

    orden_test = OrderEntity(
        id=id_dinamico, cliente_id=1, producto="Test Contract", precio=10.0, cantidad=1
    )

    with Session(engine) as session:
        repo = SQLAlchemyOrderRepository(session)

        # 2. Comprobamos la estructura (Atributos del puerto)
        assert hasattr(repo, "guardar")
        assert hasattr(repo, "obtener_por_id")
        assert hasattr(repo, "obtener_todas")

        # 3. Comprobamos el comportamiento (Insert y Select reales)
        repo.guardar(orden_test)

        # 4. Buscamos usando el mismo ID dinámico
        orden_recuperada = repo.obtener_por_id(id_dinamico)

        # 5. Validamos
        assert orden_recuperada is not None
        assert orden_recuperada.id == id_dinamico
        assert orden_recuperada.producto == "Test Contract"
