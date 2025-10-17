"""Endpoints REST para consumo y datos de clientes."""
from __future__ import annotations

from typing import cast

from flask import Blueprint, current_app, jsonify, request

from backend.services.bss_client import BSSClient, BSSClientError, BSSClientTimeout

consumption_bp = Blueprint("consumption", __name__)


def _obtener_cliente_bss() -> BSSClient:
    cliente = current_app.config.get("BSS_CLIENT")
    if cliente is None:
        current_app.logger.error("No se encontró una instancia de BSS_CLIENT en la configuración")
        raise RuntimeError("El cliente BSS no está configurado")
    return cast(BSSClient, cliente)


def _obtener_id_cliente() -> str:
    customer_id = request.args.get("customer_id")
    if not customer_id:
        raise ValueError("El parámetro de consulta 'customer_id' es obligatorio")
    return customer_id


@consumption_bp.route("/api/consumo", methods=["GET"])
def get_consumption() -> tuple:
    """Devuelve el consumo de datos y minutos del cliente indicado."""
    try:
        customer_id = _obtener_id_cliente()
        bss_client = _obtener_cliente_bss()
        payload = bss_client.get_consumption(customer_id)
        return jsonify(payload), 200
    except ValueError as error:
        return jsonify({"mensaje": str(error)}), 400
    except RuntimeError as error:
        return jsonify({"mensaje": str(error)}), 500
    except BSSClientTimeout as error:
        return jsonify({"mensaje": str(error)}), 504
    except BSSClientError as error:
        return jsonify({"mensaje": str(error)}), 404


@consumption_bp.route("/api/cliente", methods=["GET"])
def get_customer_profile() -> tuple:
    """Devuelve la información general del cliente indicado."""
    try:
        customer_id = _obtener_id_cliente()
        bss_client = _obtener_cliente_bss()
        payload = bss_client.get_customer_profile(customer_id)
        return jsonify(payload), 200
    except ValueError as error:
        return jsonify({"mensaje": str(error)}), 400
    except RuntimeError as error:
        return jsonify({"mensaje": str(error)}), 500
    except BSSClientTimeout as error:
        return jsonify({"mensaje": str(error)}), 504
    except BSSClientError as error:
        return jsonify({"mensaje": str(error)}), 404
