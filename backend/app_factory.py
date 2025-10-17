"""Factoría de aplicación y configuración global para el servicio Flask."""
from __future__ import annotations

from logging.config import dictConfig
from typing import Any, Dict

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from backend.routes.consumption import consumption_bp
from backend.services.bss_client import get_bss_client


DEFAULT_LOGGING_CONFIG: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
        }
    },
    "handlers": {
        "wsgi": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["wsgi"],
    },
}
def configure_logging(config: Dict[str, Any] | None = None) -> None:
    """Inicializa la configuración de logging."""
    logging_config = config or DEFAULT_LOGGING_CONFIG
    dictConfig(logging_config)


def configure_bss_client(app: Flask) -> None:
    """Crea y almacena una instancia del cliente BSS en la aplicación."""
    options = app.config.get("BSS_CLIENT_OPTIONS", {})
    app.config["BSS_CLIENT"] = get_bss_client(**options)


def create_app(config: Dict[str, Any] | None = None) -> Flask:
    """Crea y configura una instancia de la aplicación Flask."""
    app = Flask(__name__)

    if config:
        app.config.update(config)

    configure_logging(app.config.get("LOGGING_CONFIG"))
    configure_bss_client(app)

    register_blueprints(app)
    register_error_handlers(app)

    app.logger.debug("Aplicación inicializada con la configuración: %s", app.config)
    return app


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(consumption_bp)


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(HTTPException)
    def handle_http_exception(error: HTTPException):  # type: ignore[override]
        response = {"mensaje": error.description or "Error HTTP"}
        return jsonify(response), error.code or 500

    @app.errorhandler(Exception)
    def handle_exception(error: Exception):  # type: ignore[override]
        app.logger.exception("Excepción no controlada: %s", error)
        response = {"mensaje": "Error interno del servidor"}
        return jsonify(response), 500


__all__ = ["create_app", "configure_logging", "configure_bss_client"]
