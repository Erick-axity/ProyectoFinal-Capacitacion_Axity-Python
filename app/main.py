from fastapi import FastAPI

from app.infrastructure.api import router as orders_router


def create_app() -> FastAPI:
    """Fábrica de aplicaciones. Ideal para testing y escalabilidad."""
    app = FastAPI(
        title="Order Service",
        description="Microservicio Hexagonal para Gestión de Órdenes",
        version="1.0.0",
    )

    # Ensamblamos el router que diseñamos en la capa de infraestructura
    app.include_router(orders_router)

    @app.get("/health", tags=["System"])
    def health_check():
        return {"status": "ok", "message": "El microservicio está corriendo."}

    return app


# Instancia global para que Uvicorn la encuentre
app = create_app()
