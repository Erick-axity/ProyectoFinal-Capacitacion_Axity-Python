# ProyectoFinal-Capacitacion_Axity-Python
Proyecto final integrador tras acabar los 20 módulos de la capacitación

## Arquitectura
Este microservicio implementa Arquitectura Hexagonal (Puertos y Adaptadores) asegurando que el Dominio sea independiente del framework (FastAPI) y la Base de Datos (SQLAlchemy).

### Diagrama de Capas (Mermaid)
```mermaid
graph TD
    A[FastAPI / API Router] -->|DTO| B(Application / Use Cases)
    B -->|Inyección| C{Ports / Interfaces}
    C -->|Implementa| D[SQLAlchemy Repository]
    B -->|Reglas| E((Domain / Entities))
