"""Cliente BSS simulado.

Este módulo expone un cliente ligero que imita el comportamiento de un
Business Support System (BSS). Se utiliza desde la capa REST para recuperar
información de clientes como saldo, consumo y minutos.
"""
from __future__ import annotations

import random
import time
from typing import Dict


class BSSClientError(Exception):
    """Excepción base para errores del cliente BSS."""


class BSSClientTimeout(BSSClientError, TimeoutError):
    """Se lanza cuando el backend simulado tarda demasiado en responder."""


class BSSClient:
    """Simulación en memoria de un cliente BSS."""

    _DATA: Dict[str, Dict[str, object]] = {
        "0001": {"nombre": "Ana Pérez", "saldo": 15.5, "consumo_mb": 1024, "minutos": 120},
        "0002": {"nombre": "Luis Gómez", "saldo": 3.7, "consumo_mb": 5120, "minutos": 45},
        "0003": {"nombre": "María López", "saldo": 0.0, "consumo_mb": 256, "minutos": 300},
    }

    def __init__(self, timeout_probability: float = 0.0, latency_seconds: float = 0.0) -> None:
        self.timeout_probability = timeout_probability
        self.latency_seconds = latency_seconds

    def _simulate_latency(self) -> None:
        if self.latency_seconds:
            time.sleep(self.latency_seconds)

    def _maybe_timeout(self) -> None:
        if self.timeout_probability and random.random() < self.timeout_probability:
            raise BSSClientTimeout("Tiempo de espera agotado al consultar el servicio BSS")

    def _get_customer_record(self, customer_id: str) -> Dict[str, object]:
        self._maybe_timeout()
        self._simulate_latency()
        try:
            return self._DATA[customer_id]
        except KeyError as exc:
            raise BSSClientError(f"No se encontró el cliente '{customer_id}'") from exc

    def get_consumption(self, customer_id: str) -> Dict[str, object]:
        """Devuelve el resumen de consumo para un cliente."""
        record = self._get_customer_record(customer_id)
        return {
            "cliente_id": customer_id,
            "consumo_mb": record["consumo_mb"],
            "minutos": record["minutos"],
        }

    def get_customer_profile(self, customer_id: str) -> Dict[str, object]:
        """Devuelve la información general de un cliente."""
        record = self._get_customer_record(customer_id)
        return {
            "cliente_id": customer_id,
            "nombre": record["nombre"],
            "saldo": record["saldo"],
            "consumo_mb": record["consumo_mb"],
            "minutos": record["minutos"],
        }


def get_bss_client(timeout_probability: float = 0.0, latency_seconds: float = 0.0) -> BSSClient:
    """Ayudante para crear una instancia del cliente BSS."""
    return BSSClient(timeout_probability=timeout_probability, latency_seconds=latency_seconds)
