"""Módulo que contiene la definición de esquemas de validación de
salidas y entradas desde y hacia nuestra aplicación."""

# Librerías Externas.
from marshmallow import Schema, fields, EXCLUDE


class CreateDriverRequestSchema(Schema):
    """Clase que define el esquema esperado sobre la ruta
    de creación de Senders."""

    class Meta:
        """Clase que contiene los meta criterios."""

        unknown = EXCLUDE

    driver_id = fields.String(load_default = None)
    last_delivery = fields.String(load_default = None)


class DriverResponseSchema(Schema):
    """Clase que define el esquema para queries sobre
    entidades Sender."""

    id = fields.String(required = True)
    status = fields.String(required = True)
    last_delivery = fields.DateTime(required = True)
    created_at = fields.DateTime(required = True)
    updated_at = fields.DateTime(required = True)
