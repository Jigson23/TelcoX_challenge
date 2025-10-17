"""Fixtures de Pytest para la aplicación Flask."""
from __future__ import annotations

import pytest
from flask.testing import FlaskClient

from backend.app_factory import create_app
from backend.services.bss_client import BSSClient


@pytest.fixture
def app():
    """Crea una instancia de la aplicación con configuración de pruebas."""
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
            "BSS_CLIENT_OPTIONS": {"timeout_probability": 0.0, "latency_seconds": 0.0},
        }
    )
    yield app


@pytest.fixture
def client(app) -> FlaskClient:
    """Cliente de pruebas de Flask."""
    return app.test_client()


@pytest.fixture
def bss_client(app) -> BSSClient:
    """Devuelve la instancia del cliente BSS configurada en la app."""
    return app.config["BSS_CLIENT"]
