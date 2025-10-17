"""Pruebas de integración ligera para los endpoints de consumo."""
from __future__ import annotations

from typing import Any, Dict

import pytest
from flask import Flask

from backend.services.bss_client import BSSClient, BSSClientError, BSSClientTimeout


class DummyBSSClient(BSSClient):
    """Cliente BSS controlado para simular errores."""

    def __init__(self, *, error: Exception | None = None, payload: Dict[str, Any] | None = None) -> None:
        super().__init__(timeout_probability=0.0, latency_seconds=0.0)
        self._error = error
        self._payload = payload or {}

    def get_consumption(self, customer_id: str) -> Dict[str, Any]:
        if self._error:
            raise self._error
        return self._payload or super().get_consumption(customer_id)

    def get_customer_profile(self, customer_id: str) -> Dict[str, Any]:
        if self._error:
            raise self._error
        return self._payload or super().get_customer_profile(customer_id)


@pytest.fixture
def override_bss_client(app: Flask):
    """Permite reemplazar el cliente BSS en la app durante una prueba."""

    def _override(client: BSSClient) -> None:
        app.config["BSS_CLIENT"] = client

    return _override


def test_get_consumption_returns_data(client, override_bss_client):
    override_bss_client(BSSClient())

    response = client.get("/api/consumo", query_string={"customer_id": "0001"})

    assert response.status_code == 200
    assert response.get_json() == {"cliente_id": "0001", "consumo_mb": 1024, "minutos": 120}


def test_get_customer_profile_returns_data(client, override_bss_client):
    override_bss_client(BSSClient())

    response = client.get("/api/cliente", query_string={"customer_id": "0002"})

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["cliente_id"] == "0002"
    assert payload["nombre"] == "Luis Gómez"


def test_get_consumption_requires_customer_id(client):
    response = client.get("/api/consumo")

    assert response.status_code == 400
    assert response.get_json() == {"mensaje": "El parámetro de consulta 'customer_id' es obligatorio"}


def test_get_consumption_returns_not_found_when_bss_fails(client, override_bss_client):
    override_bss_client(DummyBSSClient(error=BSSClientError("No se encontró")))

    response = client.get("/api/consumo", query_string={"customer_id": "9999"})

    assert response.status_code == 404
    assert "No se encontró" in response.get_json()["mensaje"]


def test_get_customer_profile_returns_timeout(client, override_bss_client):
    override_bss_client(DummyBSSClient(error=BSSClientTimeout("Tiempo de espera agotado")))

    response = client.get("/api/cliente", query_string={"customer_id": "0001"})

    assert response.status_code == 504
    assert "Tiempo de espera" in response.get_json()["mensaje"]


def test_returns_500_when_bss_client_not_configured(app, client):
    app.config.pop("BSS_CLIENT", None)

    response = client.get("/api/cliente", query_string={"customer_id": "0001"})

    assert response.status_code == 500
    assert "BSS" in response.get_json()["mensaje"]
