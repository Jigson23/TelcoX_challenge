# Author: Ing. Jigson Contreras
# Email: supercontreras-ji@hotmail.com
"""Fixtures de Pytest para la aplicación Flask."""
from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest
from flask.testing import FlaskClient

from backend.app_factory import create_app
from backend.models import Billing, Consumption, Customer, db


@pytest.fixture
def app():
    """Crea una instancia de la aplicación con configuración de pruebas."""
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
        }
    )

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app) -> FlaskClient:
    """Cliente de pruebas de Flask."""
    return app.test_client()


@pytest.fixture
def sample_customer(app):
    """Crea datos de ejemplo en la base de datos para las pruebas."""
    with app.app_context():
        customer = Customer(external_id="0001", full_name="Ana Pérez", email="ana@example.com")
        db.session.add(customer)
        db.session.flush()

        db.session.add(
            Consumption(
                customer_id=customer.id,
                period_start=date(2024, 5, 1),
                period_end=date(2024, 5, 31),
                data_used_mb=1024.0,
                voice_minutes=120,
            )
        )
        db.session.add(
            Billing(
                customer_id=customer.id,
                billing_date=date(2024, 5, 15),
                amount=Decimal("15.50"),
                currency="EUR",
                due_date=date(2024, 6, 5),
                paid=False,
            )
        )
        db.session.commit()
        return customer.external_id
