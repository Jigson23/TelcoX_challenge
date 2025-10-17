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

## Variables de entorno relevantes

- **backend**
  - `FLASK_ENV`: define el entorno de ejecución de Flask (por defecto `production`).

- **frontend**
  - `NG_CLI_ANALYTICS`: desactiva la telemetría del CLI de Angular.

Puedes modificar estas variables directamente en el archivo [`docker-compose.yml`](./docker-compose.yml) según tus necesidades.
