"""Inicialización de modelos y utilidad de base de datos."""
from __future__ import annotations

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


from .customer import Billing, Consumption, Customer 


__all__ = ["db", "Customer", "Consumption", "Billing"]
