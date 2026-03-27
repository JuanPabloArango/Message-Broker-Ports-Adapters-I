"""Módulo donde definimos puntos de gestión para conexiones y elementos
de infraestructura sobre nuestra app."""

# Librerías Externas.
import os
from dotenv import load_dotenv


class Settings:
    """Clase donde encapsulamos la configuración de nuestra app."""

    load_dotenv()

    @classmethod
    def get_database_url(cls) -> str:
        """Método de clase donde generamos la URL de conexión a nuestra BD.
        
        Returns:
        ----------
        str.
            URL de conexión que reciben las sesiones de SQLAlchemy."""
        
        if os.getenv("ENVIRONMENT", "DEVELOPMENT") == "DEVELOPMENT":
            return "sqlite:///test.db"
        elif os.getenv("ENVIRONMENT") == "PRODUCTION":

            host = os.getenv("HOST")
            port = os.getenv("PORT")
            username = os.getenv("USER")
            password = os.getenv("PASSWORD")
            database = os.getenv("DATABASE")
            
            return f"postgresl://{username}:{password}@{host}:{port}/{database}"
