# Author: Ing. Jigson Contreras
# Email: supercontreras-ji@hotmail.com
"""Pruebas unitarias para los servicios de clientes."""
from __future__ import annotations

from datetime import date

import pytest

from backend.models import Consumption, Customer, db
from backend.services.customer_service import (
    CustomerNotFoundError,
    CustomerServiceError,
    get_consumption_summary,
    get_customer_profile,
)


@pytest.mark.usefixtures("app")
def test_get_consumption_summary_returns_latest_record(app):
    with app.app_context():
        customer = Customer(external_id="0001", full_name="Ana Pérez")
        db.session.add(customer)
        db.session.flush()
        db.session.add_all(
            [
                Consumption(
                    customer_id=customer.id,
                    period_start=date(2024, 4, 1),
                    period_end=date(2024, 4, 30),
                    data_used_mb=512.0,
                    voice_minutes=60,
                ),
                Consumption(
                    customer_id=customer.id,
                    period_start=date(2024, 5, 1),
                    period_end=date(2024, 5, 31),
                    data_used_mb=2048.0,
                    voice_minutes=180,
                ),
            ]
        )
        db.session.commit()

        summary = get_consumption_summary("0001")
        assert summary == {"cliente_id": "0001", "consumo_mb": 2048.0, "minutos": 180.0}


def test_get_customer_profile_includes_balance(sample_customer):
    profile = get_customer_profile(sample_customer)

    assert profile["saldo"] == 15.5
    assert profile["consumo_mb"] == 1024.0
    assert profile["minutos"] == 120.0


@pytest.mark.usefixtures("app")
def test_service_raises_when_customer_missing(app):
    with app.app_context():
        with pytest.raises(CustomerNotFoundError):
            get_customer_profile("9999")


@pytest.mark.usefixtures("app")
def test_service_raises_service_error_on_db_failure(monkeypatch, app):
    with app.app_context():
        monkeypatch.setattr("backend.services.customer_service._get_customer_by_external_id", _boom)
        with pytest.raises(CustomerServiceError):
            get_consumption_summary("0001")


def _boom(*args, **kwargs): 
    raise CustomerServiceError("fallo forzado")
