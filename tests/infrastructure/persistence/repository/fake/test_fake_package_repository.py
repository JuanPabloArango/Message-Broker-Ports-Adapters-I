"""Módulo que contiene las pruebas unitarias para el repositorio Package enfocado
en su Adapter de Fake."""

# Librerías Externas.
from typing import List

# Librerías Internas.
from app.domain.entities.package import Package

from app.domain.value_objects.id import ID
from app.domain.value_objects.package_status import PackageStatus

from app.application.ports.persistence.criteria import Criteria, Pagination, Filter, Operator

from app.infrastructure.persistence.repository.fake.package_repository import FakePackageRepositoryAdapter


class TestFakePackageRepositoryAdapter:
    """Clase que encapsula las pruebas unitarias para el adapter Fake
    del repositorio."""

    def test_repository_save(self, base_packages: List[Package]) -> None:
        """Método que contiene la prueba unitaria para validar que se
        puede almacenar una entidad de dominio en el repositorio.
        
        Args:
        ----------
        base_packages: List[Package].
            Fixture que simula una base que contiene estas entidades persistidas."""

        repository = FakePackageRepositoryAdapter(base = base_packages)

        package = Package(sender_id = ID("33"), id = "4")

        repository.save(package = package)
        retrived_package = next((package for package in repository._base if package.id.value == "4"), None)

        assert package == retrived_package, "Valida que se haya almacenado la entidad de dominio."
        assert isinstance(retrived_package, Package), "Valida que la entidad de dominio almacenada sea igual a la persistida."

    def test_repository_get(self, base_packages: List[Package]) -> None:
        """Método que contiene la prueba unitaria para validar que se puede
        obtener una entidad de dominio del repositorio.

        Args:
        ----------
        base_packages: List[Package].
            Fixture que simula una base que contiene estas entidades persistidas."""

        repository = FakePackageRepositoryAdapter(base = base_packages)

        package = repository.get(package_id = "2")

        assert isinstance(package, Package), "Valida que la entidad obtenida sea adecuada."

        assert package.driver_id == ID(value = "4"), "Valida que el estado sea el adecuado."
        assert package.status == PackageStatus.ASSIGNED, "Valida que el estado sea el adecuado."

        package = repository.get(package_id = "1")

        assert isinstance(package, Package), "Valida que la entidad obtenida sea adecuada."
        assert package.status == PackageStatus.PENDING, "Valida que el estado sea el adecuado."

    def test_list_all(self, base_packages: List[Package]) -> None:
        """Método que contiene la prueba unitaria para validar que se pueden
        filtrar y obtener varias entidades de dominio a la vez de un repositorio
        según un criterio de búsqueda.
        
        Args:
        ----------
        base_packages: List[Package].
            Fixture que simula una base que contiene estas entidades persistidas."""

        repository = FakePackageRepositoryAdapter(base = base_packages)

        criteria = Criteria(
            filters = [
                Filter(field = "status", value = PackageStatus.ASSIGNED, operator = Operator.EQ),
            ],
            pagination = Pagination(limit = 2)
        )

        filtered_packages = repository.list_all(criteria = criteria)

        assert len(filtered_packages) == 1, "Valide que el filtro se aplique correctamente."
