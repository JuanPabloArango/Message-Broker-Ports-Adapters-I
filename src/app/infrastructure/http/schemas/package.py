"""Módulo que contiene la definición de esquemas de validación de
salidas y entradas desde y hacia nuestra aplicación."""

# Librerías Externas.
from marshmallow import Schema, fields, EXCLUDE


class PackageCreationRequestSchema(Schema):
    """Clase que define el esquema esperado sobre la ruta
    de creación de Packages."""

    class Meta:
        """Clase que contiene los meta criterios."""

        unknown = EXCLUDE

    sender_id = fields.String(required = True)
    package_id = fields.String(load_default = None)


class PackageResponseSchema(Schema):
    """Clase que define el esquema para queries sobre
    entidades Package."""

    id = fields.String(required = True)
    sender_id = fields.String(required = True)
    driver_id = fields.String(required = True, allow_none = True)
    status = fields.String(required = True)
    created_at = fields.DateTime(required = True)
    updated_at = fields.DateTime(required = True)
