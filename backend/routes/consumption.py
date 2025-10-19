"""Endpoints REST para consumo y datos de clientes."""
from __future__ import annotations

from flask import Blueprint, current_app, jsonify, request

from backend.services import (
    CustomerNotFoundError,
    CustomerServiceError,
    get_consumption_summary,
    get_customer_profile,
)

consumption_bp = Blueprint("consumption", __name__)


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
        payload = get_consumption_summary(customer_id)
        return jsonify(payload), 200
    except ValueError as error:
        return jsonify({"mensaje": str(error)}), 400
    except CustomerNotFoundError as error:
        return jsonify({"mensaje": str(error)}), 404
    except CustomerServiceError as error:
        current_app.logger.exception("Error consultando consumo: %s", error)
        return jsonify({"mensaje": "Error interno del servidor"}), 500


@consumption_bp.route("/api/cliente", methods=["GET"])
def get_customer_profile_endpoint() -> tuple:
    """Devuelve la información general del cliente indicado."""
    try:
        customer_id = _obtener_id_cliente()
        payload = get_customer_profile(customer_id)
        return jsonify(payload), 200
    except ValueError as error:
        return jsonify({"mensaje": str(error)}), 400
    except CustomerNotFoundError as error:
        return jsonify({"mensaje": str(error)}), 404
    except CustomerServiceError as error:
        current_app.logger.exception("Error consultando datos de cliente: %s", error)
        return jsonify({"mensaje": "Error interno del servidor"}), 500
