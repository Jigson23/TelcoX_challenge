# Author: Ing. Jigson Contreras
# Email: supercontreras-ji@hotmail.com
"""Paquete de servicios de dominio."""
from __future__ import annotations

from .customer_service import (
    CustomerNotFoundError,
    CustomerServiceError,
    get_consumption_summary,
    get_customer_profile,
)

__all__ = [
    "CustomerNotFoundError",
    "CustomerServiceError",
    "get_consumption_summary",
    "get_customer_profile",
]
