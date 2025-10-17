"""Simulated BSS client services.

This module exposes a lightweight client that mimics the behaviour of a
Business Support System (BSS). The client is used by the REST API layer to
retrieve customer information such as balance, data consumption and minutes.
"""
from __future__ import annotations

import random
import time
from typing import Dict


class BSSClientError(Exception):
    """Base exception for BSS client errors."""


class BSSClientTimeout(BSSClientError, TimeoutError):
    """Raised when the simulated backend takes too long to respond."""


class BSSClient:
    """In-memory simulation of a BSS client."""

    _DATA: Dict[str, Dict[str, object]] = {
        "0001": {"name": "Ana Pérez", "balance": 15.5, "consumption_mb": 1024, "minutes": 120},
        "0002": {"name": "Luis Gómez", "balance": 3.7, "consumption_mb": 5120, "minutes": 45},
        "0003": {"name": "María López", "balance": 0.0, "consumption_mb": 256, "minutes": 300},
    }

    def __init__(self, timeout_probability: float = 0.0, latency_seconds: float = 0.0) -> None:
        self.timeout_probability = timeout_probability
        self.latency_seconds = latency_seconds

    def _simulate_latency(self) -> None:
        if self.latency_seconds:
            time.sleep(self.latency_seconds)

    def _maybe_timeout(self) -> None:
        if self.timeout_probability and random.random() < self.timeout_probability:
            raise BSSClientTimeout("Simulated timeout reaching the BSS service")

    def _get_customer_record(self, customer_id: str) -> Dict[str, object]:
        self._maybe_timeout()
        self._simulate_latency()
        try:
            return self._DATA[customer_id]
        except KeyError as exc:
            raise BSSClientError(f"Customer '{customer_id}' not found") from exc

    def get_consumption(self, customer_id: str) -> Dict[str, object]:
        """Return the consumption summary for a customer."""
        record = self._get_customer_record(customer_id)
        return {
            "customer_id": customer_id,
            "consumption_mb": record["consumption_mb"],
            "minutes": record["minutes"],
        }

    def get_customer_profile(self, customer_id: str) -> Dict[str, object]:
        """Return general information for a customer."""
        record = self._get_customer_record(customer_id)
        return {
            "customer_id": customer_id,
            "name": record["name"],
            "balance": record["balance"],
            "consumption_mb": record["consumption_mb"],
            "minutes": record["minutes"],
        }


def get_bss_client(timeout_probability: float = 0.0, latency_seconds: float = 0.0) -> BSSClient:
    """Factory helper to create a BSS client instance."""
    return BSSClient(timeout_probability=timeout_probability, latency_seconds=latency_seconds)
