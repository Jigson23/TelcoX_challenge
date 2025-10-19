# TelcoX Challenge

## Descripción general
La solución TelcoX ofrece un panel de control para consultar el consumo de datos y minutos de clientes de telecomunicaciones. El
backend expone una API REST construida con Flask que se conecta a una base de datos relacional mediante SQLAlchemy, mientras que el frontend se
implementa en Angular para visualizar la información en un dashboard interactivo.

## Arquitectura de la solución
- **Backend (`/backend`)**: servicio Flask con SQLAlchemy y migraciones Alembic. Expone los endpoints REST y utiliza servicios
  de dominio para recuperar la información de consumo y perfil de cliente directamente desde la base de datos.【F:backend/routes/consumption.py†L1-L45】【F:backend/services/customer_service.py†L1-L104】
- **Frontend (`/frontend/telcox-dashboard`)**: aplicación Angular 18 que consume la API y utiliza módulos PrimeNG para los
  componentes UI del panel (tablas, tarjetas, formularios y notificaciones).【F:frontend/telcox-dashboard/src/app/consumption/components/consumption-dashboard/consumption-dashboard.component.html†L1-L64】
- **Comunicación**: ambos servicios se orquestan vía `docker-compose` exponiendo el backend en el puerto 5000 y el frontend en el
  4200. En local se puede ejecutar cada servicio de forma independiente o dentro de contenedores.【F:docker-compose.yml†L1-L33】

## Requisitos previos
### Desarrollo local
- Python 3.12+ y `pip` para el backend.【F:backend/Dockerfile†L1-L16】
- Node.js 20+ y npm para el frontend.【F:frontend/Dockerfile†L1-L15】
- Angular CLI (`npm install -g @angular/cli`) para utilidades de desarrollo opcionales.