from typing import List, Optional

from sqlalchemy import Float, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from app.application.ports import OrderRepository
from app.domain.models import OrderEntity, StatusOrden

# Configuración de SQLAlchemy
DATABASE_URL = "sqlite:///orders_db.sqlite"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


class Base(DeclarativeBase):
    pass


# Modelo Físico de SQLAlchemy (Tabla)
class OrderModel(Base):
    __tablename__ = "orders"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    cliente_id: Mapped[int] = mapped_column(Integer)
    producto: Mapped[str] = mapped_column(String(100))
    precio: Mapped[float] = mapped_column(Float)
    cantidad: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(50))


# Crear tablas
Base.metadata.create_all(bind=engine)


# =====================================================================
# EL ADAPTADOR SECUNDARIO (Implementa OrderRepository)
# =====================================================================
class SQLAlchemyOrderRepository(OrderRepository):
    def __init__(self, session: Session):
        self.session = session

    def guardar(self, order: OrderEntity) -> None:
        # Convertimos la Entidad de Dominio al Modelo de Base de Datos
        db_order = OrderModel(
            id=order.id,
            cliente_id=order.cliente_id,
            producto=order.producto,
            precio=order.precio,
            cantidad=order.cantidad,
            status=order.status.value,
        )
        self.session.add(db_order)
        self.session.commit()

    def obtener_por_id(self, order_id: str) -> Optional[OrderEntity]:
        db_order = (
            self.session.query(OrderModel).filter(OrderModel.id == order_id).first()
        )
        if not db_order:
            return None

        # Reconstruimos la Entidad de Dominio para devolverla limpia
        return OrderEntity(
            id=db_order.id,
            cliente_id=db_order.cliente_id,
            producto=db_order.producto,
            precio=db_order.precio,
            cantidad=db_order.cantidad,
            status=StatusOrden(db_order.status),
        )

    def obtener_todas(self) -> List[OrderEntity]:
        db_orders = self.session.query(OrderModel).all()
        return [
            OrderEntity(
                id=o.id,
                cliente_id=o.cliente_id,
                producto=o.producto,
                precio=o.precio,
                cantidad=o.cantidad,
                status=StatusOrden(o.status),
            )
            for o in db_orders
        ]
