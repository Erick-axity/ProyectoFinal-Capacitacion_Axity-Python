from fastapi import FastAPI

# ⬅️ AQUÍ ESTÁ EL ARREGLO: Ya no pedimos 'router', solo 'orders_router' y 'auth_router'
from app.infrastructure.api import auth_router, orders_router


def create_app() -> FastAPI:
    """Fábrica de aplicaciones. Ideal para testing y escalabilidad."""
    app = FastAPI(
        title="Order Service Hexagonal",
        description="Microservicio Seguro para Gestión de Órdenes",
        version="1.0.0",
    )

    # Ensamblamos los routers que diseñamos en la capa de infraestructura
    app.include_router(auth_router)
    app.include_router(orders_router)

    @app.get("/health", tags=["System"])
    def health_check():
        return {"status": "ok", "message": "El microservicio está corriendo."}

    return app


# Instancia global para que Uvicorn la encuentre
app = create_app()
