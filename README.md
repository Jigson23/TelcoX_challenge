# TelcoX Challenge

Este repositorio contiene un backend en Flask y un frontend en Angular para el reto TelcoX. A continuación se describen los pasos para ejecutar ambos servicios usando contenedores Docker.

## Requisitos previos

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)

## Puesta en marcha con Docker Compose

1. Desde la raíz del proyecto, construye y levanta los servicios en segundo plano:

   ```bash
   docker compose up --build -d
   ```

2. Los contenedores exponen los siguientes puertos:
   - Backend Flask: [http://localhost:5000](http://localhost:5000)
   - Frontend Angular: [http://localhost:4200](http://localhost:4200)

3. Para seguir los registros de ambos servicios utiliza:

   ```bash
   docker compose logs -f
   ```

4. Cuando quieras detener y eliminar los contenedores ejecuta:

   ```bash
   docker compose down
   ```

### Migraciones de base de datos

El contenedor del backend ejecuta automáticamente las migraciones de Alembic
con `alembic upgrade head` antes de iniciar el servidor. Si necesitas
aplicarlas manualmente (por ejemplo, en un entorno local sin Docker), puedes
ejecutar:

```bash
cd backend
alembic upgrade head
```

## Variables de entorno relevantes

- **backend**
  - `FLASK_ENV`: define el entorno de ejecución de Flask (por defecto `production`).
   - `SQLALCHEMY_DATABASE_URI`: URL completa de conexión a la base de datos. Tiene
     prioridad sobre el resto de variables.
   - `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`: parámetros
     utilizados para construir la cadena de conexión MySQL cuando no se define
     `SQLALCHEMY_DATABASE_URI`.

- **frontend**
  - `NG_CLI_ANALYTICS`: desactiva la telemetría del CLI de Angular.

Puedes modificar estas variables directamente en el archivo [`docker-compose.yml`](./docker-compose.yml) según tus necesidades.
