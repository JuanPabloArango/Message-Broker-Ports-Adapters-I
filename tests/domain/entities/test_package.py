"""Módulo que contiene pruebas unitarias para la entidad de dominio Package."""

# Librerías Externas.
import pytest

# Librerías Internas.
from app.domain.entities.package import Package

from app.domain.value_objects.id import ID
from app.domain.value_objects.package_status import PackageStatus

from app.domain.exceptions import PackageTransitionError


class TestPackage:
    """Clase que encapsula las pruebas unitarias sobre la entidad Package."""

    def test_init(self) -> None:
        """Módulo que contiene la prueba unitaria que valida la instanciación
        de la entidad Package."""

        instance = Package(sender_id = ID(value = "12"), id = "321")

        assert instance.id == ID(value = "321"), "Valide que el ID sea correcto."
        assert instance.sender_id.value == "12", "Valide que siempre se requiera el ID del Sender."
        assert instance.driver_id == None, "Valide que cuando el paquete entre, no tenga asignado Driver."
        assert instance.status == PackageStatus.PENDING, "Valide que siempre un paquete entre como 'PENDING'."

    def test_create(self) -> None:
        """Módulo que contiene la prueba unitaria que valida la creación correcta
        de la entidad Package."""

        package = Package.create(sender_id = ID())

        assert isinstance(package, Package), "Valide que se esté creando la instancia correcta."
        assert len(package.id.value) == 32, "Valide que se haya generado un UUID automáticamente."
        assert len(package.sender_id.value) == 32, "Valide que se haya generado un UUID automáticamente."

    def test_assign_driver(self) -> None:
        """Módulo que contiene la prueba unitaria que se encarga de validar
        que a un paquete se le pueda asignar un conductor en situaciones correctas."""

        package = Package.create(sender_id = ID())
        package.assign_driver(driver_id = ID())

        assert package.status == PackageStatus.ASSIGNED, "Valide que cuando se asigna un Driver, cambia el estado."
        assert isinstance(package.driver_id, ID), "Valide que el ID asignado corresponda al de un Driver."

    def test_assign_driver_error(self) -> None:
        """Módulo que contiene la prueba unitaria encargada de validar que un
        paquete no se pueda asignar a un conductor en cualquier momento."""

        package = Package.create(sender_id = ID())
        package._status = PackageStatus.DELIVERED

        with pytest.raises(PackageTransitionError):
            package.assign_driver(driver_id = ID())

    def test_deliver_package(self) -> None:
        """Módulo que contiene la prueba unitaria que se encarga de validar
        que un paquete se puede marcar como entregado."""

        package = Package.create(sender_id = ID())
        assert package.status == PackageStatus.PENDING, "Valide que la transición sea la adecuada."

        package.assign_driver(driver_id = ID())
        assert package.status == PackageStatus.ASSIGNED, "Valide que la transición sea la adecuada."

        package.deliver()
        assert package.status == PackageStatus.DELIVERED, "Valide que la transición sea la adecuada."

    def test_deliver_package_error(self) -> None:
        """Módulo que contiene la prueba unitaria encargada de validar que un
        paquete no se pueda entregar en cualquier momento."""

        package = Package.create(sender_id = ID())
        package._status = PackageStatus.PENDING

        with pytest.raises(PackageTransitionError):
            package.deliver()
