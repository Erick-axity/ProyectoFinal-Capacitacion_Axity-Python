import time

from fastapi import FastAPI, Request

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

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        """Observabilidad: Inyecta el tiempo de procesamiento en los headers."""
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

    @app.get("/health", tags=["System"])
    def health_check():
        return {"status": "ok", "message": "El microservicio está corriendo."}

    return app


# Instancia global para que Uvicorn la encuentre
app = create_app()
