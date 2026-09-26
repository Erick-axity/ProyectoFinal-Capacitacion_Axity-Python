from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.ports import OrderRepository
from app.application.use_cases import CreateOrderUseCase, GetOrdersUseCase
from app.infrastructure.database import SQLAlchemyOrderRepository, engine


# Generador de sesiones de Base de Datos (Buena práctica FastAPI)
def get_db_session() -> Generator[Session, None, None]:
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()


# Fabricamos el Adaptador (Repositorio)
def get_order_repository(session: Session = Depends(get_db_session)) -> OrderRepository:
    return SQLAlchemyOrderRepository(session)


# Inyectamos el Repositorio en los Casos de Uso
def get_create_order_use_case(
    repo: OrderRepository = Depends(get_order_repository),
) -> CreateOrderUseCase:
    return CreateOrderUseCase(repo)


def get_get_orders_use_case(
    repo: OrderRepository = Depends(get_order_repository),
) -> GetOrdersUseCase:
    return GetOrdersUseCase(repo)
