"""Paquete backend para el reto TelcoX."""
from .app_factory import create_app, configure_bss_client

__all__ = ["create_app", "configure_bss_client"]
