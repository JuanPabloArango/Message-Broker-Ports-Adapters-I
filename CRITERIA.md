# Patrón Criteria

El patrón Criteria permite expresar condiciones de filtrado (`=`, `<`, `>`, `IN`, `CONTAINS`, etc.)
como objetos, en lugar de parámetros sueltos en el repositorio.

Vive en `application/ports/persistence/` porque es una abstracción — no depende de SQL ni de ningún
framework. Cada implementación del repositorio lo traduce a su propia tecnología.

---

## Archivos y responsabilidades

### `application/ports/persistence/criteria.py`
Define las estructuras base del patrón. No importa nada de infraestructura.

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Operator(Enum):
    EQ = "eq"
    NEQ = "neq"
    LT = "lt"
    LTE = "lte"
    GT = "gt"
    GTE = "gte"
    IN = "in"
    CONTAINS = "contains"


@dataclass(frozen=True)
class Filter:
    field: str
    operator: Operator
    value: Any


@dataclass(frozen=True)
class Criteria:
    filters: list[Filter] = field(default_factory=list)
```

---

### `application/queries/list_packages.py`
La Query transporta el Criteria hacia el handler. No construye ni valida nada.

```python
from dataclasses import dataclass
from app.application.queries.base import Query
from app.application.ports.persistence.criteria import Criteria


@dataclass(frozen=True)
class ListPackages(Query):
    criteria: Criteria
```

---

### `application/query_handlers/list_packages_handler.py`
El handler recibe la Query y delega al repositorio. No sabe nada de filtros ni de SQL.

```python
from app.application.queries.list_packages import ListPackages
from app.application.ports.persistence.uow import UnitOfWorkPort
from app.domain.entities.package import Package


class ListPackagesHandler:
    def __init__(self, uow: UnitOfWorkPort) -> None:
        self._uow = uow

    def handle(self, query: ListPackages) -> list[Package]:
        with self._uow:
            return self._uow.package_repository.list_all(query.criteria)
```

---

### `application/ports/persistence/repositories/package_repository.py`
El puerto define el contrato. Acepta Criteria, no parámetros sueltos.

```python
from abc import ABC, abstractmethod
from app.domain.entities.package import Package
from app.application.ports.persistence.criteria import Criteria


class PackageRepositoryPort(ABC):
    @abstractmethod
    def list_all(self, criteria: Criteria) -> list[Package]: ...
```

---

### `infrastructure/persistence/repository/sql/package_repository.py`
Traduce el Criteria a filtros SQLAlchemy.

```python
from app.application.ports.persistence.criteria import Criteria, Operator
from app.domain.entities.package import Package
from app.infrastructure.persistence.orm.tables.package import PackageTable


OPERATOR_MAP = {
    Operator.EQ:       lambda col, val: col == val,
    Operator.NEQ:      lambda col, val: col != val,
    Operator.LT:       lambda col, val: col < val,
    Operator.LTE:      lambda col, val: col <= val,
    Operator.GT:       lambda col, val: col > val,
    Operator.GTE:      lambda col, val: col >= val,
    Operator.IN:       lambda col, val: col.in_(val),
    Operator.CONTAINS: lambda col, val: col.contains(val),
}


class SqlPackageRepository(PackageRepositoryPort):
    def __init__(self, session) -> None:
        self._session = session

    def list_all(self, criteria: Criteria) -> list[Package]:
        q = self._session.query(PackageTable)

        for f in criteria.filters:
            column = getattr(PackageTable, f.field)
            condition = OPERATOR_MAP[f.operator](column, f.value)
            q = q.filter(condition)

        return [mapper.to_domain(row) for row in q.all()]
```

---

### `infrastructure/persistence/repository/fake/package_repository.py`
Aplica los mismos filtros en memoria, sin SQL.

```python
from typing import Any
from app.application.ports.persistence.criteria import Criteria, Operator
from app.domain.entities.package import Package


class FakePackageRepository(PackageRepositoryPort):
    def __init__(self) -> None:
        self._packages: dict[str, Package] = {}

    def list_all(self, criteria: Criteria) -> list[Package]:
        result = list(self._packages.values())

        for f in criteria.filters:
            result = [
                p for p in result
                if self._apply(getattr(p, f.field), f.operator, f.value)
            ]

        return result

    def _apply(self, attr: Any, operator: Operator, value: Any) -> bool:
        match operator:
            case Operator.EQ:       return attr == value
            case Operator.NEQ:      return attr != value
            case Operator.LT:       return attr < value
            case Operator.LTE:      return attr <= value
            case Operator.GT:       return attr > value
            case Operator.GTE:      return attr >= value
            case Operator.IN:       return attr in value
            case Operator.CONTAINS: return value in attr
```

---

### `infrastructure/http/dtos/package.py`
El DTO de respuesta representa un Package serializado. La entidad de dominio nunca sale cruda.

```python
from dataclasses import dataclass
from app.domain.entities.package import Package


@dataclass
class PackageResponse:
    id: str
    sender_id: str
    driver_id: str | None
    status: str

    @classmethod
    def from_domain(cls, package: Package) -> "PackageResponse":
        return cls(
            id=str(package.id.value),
            sender_id=str(package.sender_id.value),
            driver_id=str(package.driver_id.value) if package.driver_id else None,
            status=package.status.value,
        )
```

---

### `infrastructure/http/routes/packages.py`
El entry point recibe el GET request, construye el Criteria desde los query params,
arma la Query y convierte el resultado a DTOs.

```python
from flask import request, jsonify
from app.application.ports.persistence.criteria import Criteria, Filter, Operator
from app.application.queries.list_packages import ListPackages
from app.application.query_handlers.list_packages_handler import ListPackagesHandler
from app.infrastructure.http.dtos.package import PackageResponse


@app.route("/packages", methods=["GET"])
def list_packages():
    filters = []

    # GET /packages?status=PENDING
    if status := request.args.get("status"):
        filters.append(Filter(field="status", operator=Operator.EQ, value=status))

    # GET /packages?statuses=PENDING,ASSIGNED
    if statuses := request.args.get("statuses"):
        filters.append(Filter(field="status", operator=Operator.IN, value=statuses.split(",")))

    # GET /packages?sender_id=abc-123
    if sender_id := request.args.get("sender_id"):
        filters.append(Filter(field="sender_id", operator=Operator.EQ, value=sender_id))

    query = ListPackages(criteria=Criteria(filters=filters))
    packages = ListPackagesHandler(uow).handle(query)

    return jsonify([PackageResponse.from_domain(p).__dict__ for p in packages]), 200
```

---

## Flujo completo

```
GET /packages?status=PENDING&sender_id=abc-123
        |
        v
 route lee query params
        |
        v
 construye Criteria([
     Filter("status",    Operator.EQ, "PENDING"),
     Filter("sender_id", Operator.EQ, "abc-123"),
 ])
        |
        v
 ListPackages(criteria=Criteria(...))   <-- Query
        |
        v
 ListPackagesHandler.handle(query)
        |
        v
 package_repository.list_all(criteria)  <-- puerto
        |
        v
 SQL: WHERE status = 'PENDING' AND sender_id = 'abc-123'
 Fake: filtra la lista en memoria
        |
        v
 list[Package]   <-- entidades de dominio
        |
        v
 [PackageResponse.from_domain(p) for p in packages]  <-- DTOs
        |
        v
 JSON response
```

---

## Regla para saber dónde agregar un nuevo operador

1. Agregar el valor en `Operator` (enum en `criteria.py`).
2. Agregar la lambda en `OPERATOR_MAP` del repositorio SQL.
3. Agregar el caso en `_apply` del repositorio fake.
4. El resto del código no cambia.
