# Author: Ing. Jigson Contreras
# Email: supercontreras-ji@hotmail.com
"""Servicios de consulta de clientes respaldados por base de datos."""
from __future__ import annotations

from decimal import Decimal
from typing import Dict

from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError

from backend.models import Billing, Consumption, Customer, db


class CustomerServiceError(Exception):
    """Error genérico al interactuar con la capa de datos."""


class CustomerNotFoundError(CustomerServiceError):
    """Se lanza cuando no existe un cliente con el identificador indicado."""

    def __init__(self, external_id: str) -> None:
        super().__init__(f"No se encontró el cliente '{external_id}'")
        self.external_id = external_id


def _get_customer_by_external_id(external_id: str) -> Customer:
    """Recupera un cliente por su identificador externo o lanza un error."""

    session = db.session
    customer = session.execute(
        select(Customer).where(Customer.external_id == external_id)
    ).scalar_one_or_none()
    if customer is None:
        raise CustomerNotFoundError(external_id)
    return customer


def _get_latest_consumption(customer_id: int) -> Consumption | None:
    """Obtiene el registro de consumo más reciente para un cliente."""

    session = db.session
    return (
        session.execute(
            select(Consumption)
            .where(Consumption.customer_id == customer_id)
            .order_by(Consumption.period_end.desc(), Consumption.id.desc())
        )
        .scalars()
        .first()
    )


def _calculate_outstanding_balance(customer_id: int) -> float:
    """Calcula el saldo pendiente a partir de facturas no pagadas."""

    session = db.session
    raw_balance: Decimal | float | None = session.execute(
        select(func.coalesce(func.sum(Billing.amount), 0))
        .where(Billing.customer_id == customer_id, Billing.paid.is_(False))
    ).scalar_one()
    if raw_balance is None:
        return 0.0
    return float(raw_balance)


def get_consumption_summary(external_id: str) -> Dict[str, float | str]:
    """Devuelve el consumo de datos y minutos para un cliente."""

    try:
        customer = _get_customer_by_external_id(external_id)
        latest_consumption = _get_latest_consumption(customer.id)

        data_used = float(latest_consumption.data_used_mb) if latest_consumption else 0.0
        minutes = float(latest_consumption.voice_minutes) if latest_consumption else 0.0

        return {
            "cliente_id": customer.external_id,
            "consumo_mb": data_used,
            "minutos": minutes,
        }
    except CustomerServiceError:
        raise
    except SQLAlchemyError as exc:
        raise CustomerServiceError("Error al consultar el consumo del cliente") from exc


def get_customer_profile(external_id: str) -> Dict[str, float | str]:
    """Devuelve la información general de un cliente."""

    try:
        customer = _get_customer_by_external_id(external_id)
        latest_consumption = _get_latest_consumption(customer.id)
        balance = _calculate_outstanding_balance(customer.id)

        data_used = float(latest_consumption.data_used_mb) if latest_consumption else 0.0
        minutes = float(latest_consumption.voice_minutes) if latest_consumption else 0.0

        return {
            "cliente_id": customer.external_id,
            "nombre": customer.full_name,
            "saldo": balance,
            "consumo_mb": data_used,
            "minutos": minutes,
        }
    except CustomerServiceError:
        raise
    except SQLAlchemyError as exc:
        raise CustomerServiceError("Error al consultar los datos del cliente") from exc


__all__ = [
    "CustomerServiceError",
    "CustomerNotFoundError",
    "get_consumption_summary",
    "get_customer_profile",
]
