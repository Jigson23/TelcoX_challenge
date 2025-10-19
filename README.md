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

### Contenedores
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)

## Puesta en marcha
### Con Docker Compose
1. Construir y levantar los servicios desde la raíz del proyecto:
   ```bash
   docker compose up --build -d
   ```
2. Acceder a los servicios:
   - Backend Flask: http://localhost:5000
   - Frontend Angular: http://localhost:4200
3. Seguir los registros combinados:
   ```bash
   docker compose logs -f
   ```
4. Detener y limpiar los contenedores:
   ```bash
   docker compose down
   ```

### Backend Flask en local
1. Crear y activar un entorno virtual:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # En Windows: .venv\\Scripts\\activate
   ```
2. Instalar dependencias y preparar la base de datos (SQLite por defecto, configurable vía variables):
   ```bash
   pip install -r requirements.txt
   alembic upgrade head
   ```
3. Definir las variables necesarias si se usa una base MySQL externa (`DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` o
   `SQLALCHEMY_DATABASE_URI`).【F:backend/app_factory.py†L31-L58】
4. Ejecutar la aplicación:
   ```bash
   FLASK_ENV=development python -m backend.app
   ```

Al ejecutar `alembic upgrade head` se crean las tablas y se insertan tres clientes de ejemplo con consumos y facturación pendientes para poder probar la integración de extremo a extremo.【F:backend/migrations/versions/4c8d2df1a1a0_seed_initial_data.py†L1-L87】

### Frontend Angular en local
1. Instalar dependencias:
   ```bash
   cd frontend/telcox-dashboard
   npm install
   ```
2. Levantar el servidor de desarrollo:
   ```bash
   npm start
   ```
3. El panel estará disponible en http://localhost:4200 y recargará automáticamente ante cambios.

## Referencia de API
| Endpoint | Método | Parámetros | Respuesta exitosa |
| --- | --- | --- | --- |
| `/api/consumo` | GET | `customer_id` (query string, obligatorio) | Resumen de consumo del cliente: `cliente_id`, `consumo_mb`, `minutos`.【F:backend/routes/consumption.py†L24-L37】【F:backend/services/customer_service.py†L44-L68】 |
| `/api/cliente` | GET | `customer_id` (query string, obligatorio) | Perfil completo del cliente: `cliente_id`, `nombre`, `saldo`, `consumo_mb`, `minutos`.【F:backend/routes/consumption.py†L39-L45】【F:backend/services/customer_service.py†L71-L104】 |