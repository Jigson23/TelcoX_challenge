"""Pruebas unitarias para el cliente BSS simulado."""
from __future__ import annotations

import pytest

from backend.services.bss_client import BSSClient, BSSClientError, BSSClientTimeout


def test_get_consumption_returns_expected_payload():
    client = BSSClient()

    result = client.get_consumption("0001")

    assert result == {"cliente_id": "0001", "consumo_mb": 1024, "minutos": 120}


def test_get_customer_profile_returns_expected_payload():
    client = BSSClient()

    result = client.get_customer_profile("0002")

    assert result["cliente_id"] == "0002"
    assert result["nombre"] == "Luis Gómez"
    assert result["saldo"] == 3.7


def test_get_customer_profile_raises_error_when_missing():
    client = BSSClient()

    with pytest.raises(BSSClientError):
        client.get_customer_profile("9999")


def test_get_consumption_raises_timeout_when_probability_is_one():
    client = BSSClient(timeout_probability=1.0)

    with pytest.raises(BSSClientTimeout):
        client.get_consumption("0001")
