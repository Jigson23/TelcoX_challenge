# Author: Ing. Jigson Contreras
# Email: supercontreras-ji@hotmail.com
"""Pruebas de integración ligera para los endpoints de consumo."""
from __future__ import annotations

from typing import Any, Dict

import pytest


@pytest.mark.usefixtures("sample_customer")
def test_get_consumption_returns_data(client):
    response = client.get("/api/consumo", query_string={"customer_id": "0001"})

    assert response.status_code == 200
    assert response.get_json() == {"cliente_id": "0001", "consumo_mb": 1024.0, "minutos": 120.0}


@pytest.mark.usefixtures("sample_customer")
def test_get_customer_profile_returns_data(client):
    response = client.get("/api/cliente", query_string={"customer_id": "0001"})

    assert response.status_code == 200
    payload: Dict[str, Any] = response.get_json()
    assert payload == {
        "cliente_id": "0001",
        "nombre": "Ana Pérez",
        "saldo": 15.5,
        "consumo_mb": 1024.0,
        "minutos": 120.0,
    }


def test_get_consumption_requires_customer_id(client):
    response = client.get("/api/consumo")

    assert response.status_code == 400
    assert response.get_json() == {"mensaje": "El parámetro de consulta 'customer_id' es obligatorio"}


@pytest.mark.usefixtures("sample_customer")
def test_get_consumption_returns_not_found_when_customer_missing(client):
    response = client.get("/api/consumo", query_string={"customer_id": "9999"})

    assert response.status_code == 404
    assert "No se encontró" in response.get_json()["mensaje"]


@pytest.mark.usefixtures("sample_customer")
def test_get_customer_profile_returns_not_found_when_customer_missing(client):
    response = client.get("/api/cliente", query_string={"customer_id": "9999"})

    assert response.status_code == 404
    assert "No se encontró" in response.get_json()["mensaje"]
