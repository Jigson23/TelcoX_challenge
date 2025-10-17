"""REST endpoints for customer consumption and profile data."""
from __future__ import annotations

from flask import Blueprint, jsonify, request

from backend.services.bss_client import BSSClientError, BSSClientTimeout, get_bss_client

consumption_bp = Blueprint("consumption", __name__)
_bss_client = get_bss_client()


def _get_customer_id() -> str:
    customer_id = request.args.get("customer_id")
    if not customer_id:
        raise ValueError("The 'customer_id' query parameter is required")
    return customer_id


@consumption_bp.route("/api/consumo", methods=["GET"])
def get_consumption() -> tuple:
    """Return data consumption information for the given customer."""
    try:
        customer_id = _get_customer_id()
        payload = _bss_client.get_consumption(customer_id)
        return jsonify(payload), 200
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except BSSClientTimeout as error:
        return jsonify({"error": str(error)}), 504
    except BSSClientError as error:
        return jsonify({"error": str(error)}), 404


@consumption_bp.route("/api/cliente", methods=["GET"])
def get_customer_profile() -> tuple:
    """Return the customer profile."""
    try:
        customer_id = _get_customer_id()
        payload = _bss_client.get_customer_profile(customer_id)
        return jsonify(payload), 200
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except BSSClientTimeout as error:
        return jsonify({"error": str(error)}), 504
    except BSSClientError as error:
        return jsonify({"error": str(error)}), 404
