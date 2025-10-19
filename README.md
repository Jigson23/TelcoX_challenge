# TelcoX Challenge

## Descripción general
La solución TelcoX ofrece un panel de control para consultar el consumo de datos y minutos de clientes de telecomunicaciones. El
backend expone una API REST construida con Flask que se conecta a una base de datos relacional mediante SQLAlchemy, mientras que el frontend se
implementa en Angular para visualizar la información en un dashboard interactivo.

## Arquitectura de la solución
- **Backend (`/backend`)**: servicio Flask con SQLAlchemy y migraciones Alembic. Expone los endpoints REST y utiliza servicios
  de dominio para recuperar la información de consumo y perfil de cliente directamente desde la base de datos.【F:backend/routes/consumption.py†L1-L45】【F:backend/services/customer_service.py†L1-L104】