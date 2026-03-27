"""Módulo que contiene las pruebas unitarias para el Object Relational Mapping
entre la entidad de dominio Package y su tabla de persistencia."""

# Librerías Externas.
import datetime as dt

from sqlalchemy import text
from sqlalchemy.orm import Session

# Librerías Internas.
from app.domain.entities.package import Package

from app.domain.value_objects.id import ID
from app.domain.value_objects.package_status import PackageStatus


class TestPackageORM:
    """Clase que encapsula las pruebas unitarias del ORM de Sender."""

    def test_package_insertion(self, test_session: Session) -> None:
        """Método que contiene la prueba unitaria para validar la correcta
        inserción de entidades de dominio.
        
        Args:
        ----------
        test_session: Session.
            Sesión de conexión a BD."""

        stmt = """
        INSERT INTO packages (id, sender_id, driver_id, status, created_at, updated_at)
        VALUES (:id, :sender_id, :driver_id, :status, :created_at, :updated_at)
        """

        test_session.execute(text(stmt), {"id": "1",
                                          "sender_id": "12",
                                          "driver_id": None,
                                          "status": "PENDING",
                                          "created_at": dt.datetime(2024, 4, 8, 10, 10, 10),
                                          "updated_at": dt.datetime(2024, 4, 8, 10, 10, 10)})
        
        package = test_session.get(Package, "1")

        assert isinstance(package, Package), "Valide que el registro de la tabla si se haya mapeado a entidad de dominio."

        assert package.id.value == "1", "Valide que el ID obtenido corresponda con el ID almacenado."
        assert package.sender_id.value == "12", "Valide que el ID obtenido corresponda con el ID almacenado."
        assert not package.driver_id, "Valide que el ID obtenido corresponda con el ID almacenado."
        assert package.status == PackageStatus.PENDING, "Valide que el valor de persistencia se mapee a valor de domini."

    def test_package_bulk_insertion(self, test_session: Session) -> None:
        """Método que contiene la prueba unitaria para validar la correcta
        inserción masiva de entidades de dominio.
        
        Args:
        ----------
        test_session: Session.
            Sesión de conexión a BD."""

        stmt = """
        INSERT INTO packages (id, sender_id, driver_id, status, created_at, updated_at)
        VALUES ("1", "1", null, "PENDING", "2024-10-10 23:23:23", "2024-10-10 23:23:23"),
               ("2", "1", "43", "ASSIGNED", "2024-10-10 23:23:23", "2024-11-10 23:23:23"),
               ("3", "3", "14", "DELIVERED", "2024-10-10 23:23:23", "2024-11-10 23:23:23");
        """

        test_session.execute(text(stmt))

        package = test_session.get(Package, "2")
        packages = test_session.query(Package).all()

        assert len(packages) == 3, "Valide que la cantidad de filas en persistencia se represente en cantidad de entidades de dominio."
        
        assert all(isinstance(package, Package) for package in packages), "Valide que se carguen las entidades de dominio correctas."

        assert package.driver_id == ID(value = "43"), "Valide que los IDs de conductores se asignen correctamente."

    def test_package_retrieval(self, test_session: Session) -> None:
        """Método que contiene la prueba unitaria para validar la correcta
        extracción de una entidad de dominio.
        
        Args:
        ----------
        test_session: Session.
            Sesión de conexión a BD."""

        package = Package(id = "5", sender_id = ID("43"))

        test_session.add(package)
        test_session.commit()

        stmt = """
        SELECT id, sender_id, driver_id, status
        FROM packages;
        """

        row = test_session.execute(text(stmt)).one()

        assert row == ("5", "43", None, "PENDING"), "Valide que los valores de dominio hayan sido mapeados a tablas."

    def test_package_bulk_retrieval(self, test_session: Session) -> None:
        """Método que contiene la prueba unitaria para validar la correcta
        extracción de varias entidades de dominio.
        
        Args:
        ----------
        test_session: Session.
            Sesión de conexión a BD."""

        package1 = Package(id = "23", sender_id = ID("1"))
        package2 = Package(id = "24", sender_id = ID("2"))
        package3 = Package(id = "25", sender_id = ID("3"))
        package3.assign_driver(driver_id = ID("42"))

        test_session.add_all((package1, package2, package3))
        test_session.commit()

        stmt = """
        SELECT id, sender_id, driver_id, status
        FROM packages
        ORDER BY id;
        """

        rows = test_session.execute(text(stmt)).all()

        assert len(rows) == 3, "Valide que la cantidad de filas corresponda a la cantidad de entidades de dominio."
        assert rows == [("23", "1", None, "PENDING"),
                        ("24", "2", None, "PENDING"),
                        ("25", "3", "42", "ASSIGNED")], "Valide los valores persistidos."

    def test_package_update(self, test_session: Session) -> None:
        """Método que contiene la prueba unitaria para validar que la actualización
        de una entidad se puede ver reflejada en su persistencia.
        
        Args:
        ----------
        test_session: Session.
            Sesión de conexión a BD."""

        created_package = Package(id = "42", sender_id = ID("56"))

        test_session.add(created_package)
        test_session.commit()

        retrieved_package = test_session.get(Package, "42")

        assert not retrieved_package.driver_id, "Valide el estado actual de persistencia."
        assert retrieved_package.status == PackageStatus.PENDING, "Valide el estado actual de persistencia."

        assert created_package == retrieved_package, "Valide que la entidad de dominio persistida y cargada sean iguales."
        
        retrieved_package.assign_driver(driver_id = "100")
        test_session.commit()

        retrieved_package = test_session.get(Package, "42")

        assert retrieved_package.driver_id, "Valide la correcta transición de estados."
        assert retrieved_package.status == PackageStatus.ASSIGNED, "Valide la correcta transición de estados."

    def test_package_deletion(self, test_session: Session) -> None:
        """Método que contiene la prueba unitaria para validar la correcta
        eliminación de una entidad de dominio.
        
        Args:
        ----------
        test_session: Session.
            Sesión de conexión a BD."""

        created_package = Package(id = "42", sender_id = ID("56"))

        test_session.add(created_package)
        test_session.commit()

        retrieved_package = test_session.get(Package, "42")

        assert created_package == retrieved_package, "Valide que la entidad de dominio persistida y cargada sean iguales."

        test_session.delete(retrieved_package)
        test_session.commit()

        stmt = """
        SELECT COUNT(*)
        FROM packages;
        """

        count = test_session.execute(text(stmt)).scalar()

        assert count == 0, "Valide que la eliminación de registros sea posible."
