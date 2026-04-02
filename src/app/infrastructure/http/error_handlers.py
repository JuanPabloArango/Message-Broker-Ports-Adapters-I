"""Módulo que se encarga de registrar todos los posibles errores que pueden
ocurrir en nuestra aplicación."""

# Librerías Externas.
from typing import Type, Dict, Tuple, Callable

from flask import Flask

# Librerías Internas.
from app.domain.exceptions import (
    DomainException,
    DeliveryDateError,
    SenderAlreadyVerified,
    SenderNotVerified,
    PackageTransitionError,
    DriverCurrenlyOccupiedError,
    DriverAlreadyAvailableError,
)

from app.application.exceptions import (
    ApplicationException,
    NotAValidAttribute,
    SenderNotFound,
    DriverNotFound,
    PackageNotFound,
    NotCurrenltyAvailableDrivers
)


class ErrorHandler:
    """Clase que encapsula todos los posibles errores de nuestra aplicación
    en un solor lugar."""

    _MAP: Dict[Type[Exception], int] = {
        # 400
        NotAValidAttribute: 400,
        DeliveryDateError: 400,
        # 404
        SenderNotFound: 404,
        DriverNotFound: 404,
        PackageNotFound: 404,
        # 409
        SenderAlreadyVerified: 409,
        PackageTransitionError: 409,
        DriverCurrenlyOccupiedError: 409,
        DriverAlreadyAvailableError: 409,
        NotCurrenltyAvailableDrivers: 409,
        # 422
        SenderNotVerified: 422
    }

    @classmethod
    def register(cls, app: Flask) -> None:
        """Método que permite registro dinámico de nuestros
        errores de aplicación.
        
        Args:
        ----------
        app: Flask.
            Aplicación donde se mapearán los errores."""

        for exc_cls, exc_status_code in cls._MAP.items():
            app.errorhandler(exc_cls)(cls._make_handler(exc_status_code))

        app.errorhandler(DomainException)(cls._make_handler(422))
        app.errorhandler(ApplicationException)(cls._make_handler(400))
        app.errorhandler(Exception)(cls._make_handler(500))

    @classmethod
    def _make_handler(cls, status_code: int) -> Callable[[Exception], Tuple[Dict[str, str], int]]:
        """Método de clase que funciona como decorador para generalizar el
        patrón:
        
        @app.errorhandler(NotAValidAttribute)
        def handle_invalid_attribute(e: NotAValidAttribute):
            return {"error": str(e)}, 400
        
        Args:
        ----------
        status_code: int.
            Código de estado del error.
            
        Returns:
        ----------
        Callable[[Exception], Tuple[Dict[str, str], int]].
            Función que retornará el mensaje."""

        def handler(e: Exception) -> Tuple[Dict[str, str], int]:
            """Función que invoca el decorador @app.errorhandler
            al ver la excepción.
            
            Args:
            ----------
            e: Exception.
                Excepción ocurrida en la app.
                
            Returns:
            ----------
            Dict[str, str].
                Mensaje de error que verá el usuario.
            
            int.
                Código de estado del error."""

            return {"error": str(e)}, status_code

        return handler
