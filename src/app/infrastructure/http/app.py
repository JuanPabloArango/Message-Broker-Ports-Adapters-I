"""Módulo que contiene la definición de nuestra aplicación HTTP."""

# Librerías Externas.
from typing import Optional

from flask import Flask
from flask_smorest import Api

# Librerías Internas.
from app.application.ports.persistence.uow import UnitOfWorkPort

from app.infrastructure.bootstrap import bootstrap
from app.infrastructure.http.error_handlers import ErrorHandler

from app.infrastructure.http.views.sender import blp as SenderBlueprint
from app.infrastructure.http.views.driver import blp as DriverBlueprint
from app.infrastructure.http.views.package import blp as PackageBlueprint


def create_app(unit_of_work: Optional[UnitOfWorkPort] = None) -> Flask:
    """Método factory para crear la aplicación.

    Args:
    ----------
    unit_of_work: Optional[UnitOfWorkPort].
        Unidad de trabajo.
    
    Returns:
    ----------
    Flask.
        Aplicación web."""
    
    app = Flask(__name__)

    app.config["API_TITLE"] = "Message Broker Exercise"
    app.config["API_VERSION"] = "1.0.0-test.1"
    app.config["OPENAPI_VERSION"] = "3.0.1"

    bootstrap(unit_of_work = unit_of_work)
    ErrorHandler.register(app = app)

    api = Api(app = app)
    api.register_blueprint(SenderBlueprint)
    api.register_blueprint(DriverBlueprint)
    api.register_blueprint(PackageBlueprint)

    return app
