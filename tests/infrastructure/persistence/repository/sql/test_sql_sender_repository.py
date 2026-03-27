"""Módulo que contiene las pruebas unitarias para el repositorio Package enfocado
en su Adapter de SQLAlchemy."""

# Librerías Externas.
import pytest

from sqlalchemy import text
from sqlalchemy.orm import Session

# Librerías Internas.
from app.domain.entities.sender import Sender

from app.domain.value_objects.id import ID
from app.domain.value_objects.sender_status import SenderStatus

from app.application.ports.persistence.criteria import Criteria, Filter, Operator
from app.application.exceptions import NotAValidAttribute

from app.infrastructure.persistence.repository.sql.sender_repository import SQLSenderRepositoryAdapter


class TestSQLSenderRepositoryAdapter:
    """Clase que encapsula las pruebas unitarias de la clase.
    SQLSenderRepositoryAdapter."""

    def test_repository_save(self, test_session: Session) -> None:
        """Método que contiene la prueba unitaria para validar adición de
        entidades al repositorio.
        
        Args:
        ----------
        test_session: Session.
            Sesión de conexión a BD."""
        
        repository = SQLSenderRepositoryAdapter(session = test_session)

        sender = Sender(id = "42")

        repository.save(sender)
        test_session.commit()

        stmt = """
        SELECT id, status
        FROM senders
        WHERE id = "42";
        """

        row = test_session.execute(text(stmt)).one_or_none()

        assert row == ("42", "UNVERIFIED"), "Valide que su repositorio sirva para almacenar entidades en BD."

    def test_repository_get(self, test_session: Session) -> None:
        """Método que contiene la prueba unitaria para validar adición de
        entidades al repositorio.
        
        Args:
        ----------
        test_session: Session.
            Sesión de conexión a BD."""
        
        repository = SQLSenderRepositoryAdapter(session = test_session)

        stmt = """
        INSERT INTO senders (id, status, created_at, updated_at)
        VALUES ("1", "VERIFIED", "2025-10-01 14:15:16", "2025-10-04 14:15:16"),
               ("2", "UNVERIFIED", "2025-10-01 14:15:16", "2025-10-04 14:15:16");
        """

        test_session.execute(text(stmt))

        sender = repository.get(sender_id = "1")

        assert isinstance(sender, Sender), "Valide que su repositorio pueda obtener entidades."

        assert sender.id == ID(value = "1"), "Valide que su obtención de entidades contenga los atributos adecuados."
        assert sender.status == SenderStatus.VERIFIED, "Valide que su obtención de entidades contenga los atributos adecuados."

    def test_repository_list_all(self, test_session: Session) -> None:
        """Método que contiene la prueba unitaria para validar 
        que se puedan listar entidades.

        Args:
        ----------
        test_session: Session.
            Sesión de conexión a BD."""
        
        repository = SQLSenderRepositoryAdapter(session = test_session)

        stmt = """
        INSERT INTO senders (id, status, created_at, updated_at)
        VALUES ("1", "VERIFIED", "2026-03-26 01:00:00", "2026-03-26 02:00:00"),
               ("2", "UNVERIFIED", "2026-03-26 01:00:00", "2026-03-26 01:00:00"),
               ("3", "VERIFIED", "2026-03-26 02:00:00", "2026-03-26 03:00:00"),
               ("4", "UNVERIFIED", "2026-03-26 02:00:00", "2026-03-26 02:00:00"),
               ("5", "VERIFIED", "2026-03-26 03:00:00", "2026-03-26 04:00:00");
        """

        test_session.execute(text(stmt))

        filter = Filter(field = "status", value = "VERIFIED", operator = Operator.NEQ)
        criteria = Criteria(filters = [filter])

        verified_senders = repository.list_all(criteria = criteria)

        assert len(verified_senders) == 2, "Valide que sus operadores funcionen correctamente."

        filter = Filter(field = "invalid_field", value = "VERIFIED", operator = Operator.NEQ)
        criteria = Criteria(filters = [filter])

        with pytest.raises(NotAValidAttribute):
            repository.list_all(criteria = criteria)