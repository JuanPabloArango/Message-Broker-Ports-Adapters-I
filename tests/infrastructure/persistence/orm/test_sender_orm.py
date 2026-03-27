"""Módulo que contiene las pruebas unitarias para el Object Relational Mapping
entre la entidad de dominio Sender y su tabla de persistencia."""

# Librerías Externas.
import datetime as dt

from sqlalchemy import text
from sqlalchemy.orm import Session

# Librerías Internas.
from app.domain.entities.sender import Sender

from app.domain.value_objects.id import ID
from app.domain.value_objects.sender_status import SenderStatus


class TestSenderORM:
    """Clase que encapsula las pruebas unitarias del ORM de Sender."""

    def test_sender_insertion(self, test_session: Session) -> None:
        """Método que contiene la prueba unitaria para validar la correcta
        inserción de entidades de dominio.
        
        Args:
        ----------
        test_session: Session.
            Sesión de conexión a BD."""

        stmt = """
        INSERT INTO senders (id, status, created_at, updated_at)
        VALUES (:sender_id, :sender_status, :created_at, :updated_at);
        """

        test_session.execute(text(stmt), {"sender_id": "123",
                                          "sender_status": "VERIFIED",
                                          "created_at": dt.datetime(2023, 4, 11, 14, 14, 14),
                                          "updated_at": dt.datetime(2023, 4, 11, 15, 0, 0)})
        
        sender = test_session.get(Sender, "123")

        assert isinstance(sender, Sender), "Valida que las filas de la tabla se mapean a entidades de dominio correctas."

        assert isinstance(sender.id, ID), "Valide que las columnas se mapean al typing correcto."
        assert isinstance(sender.status, SenderStatus), "Valide que las columnas se mapean al typing correcto."

        assert sender.id.value == "123", "Valide que el ID persistido sea el mismo que el ID creado."
        assert sender.status.value == "VERIFIED", "Valide que el estado persistido sea el mismo que el estado creado."

        assert isinstance(sender._created_at, dt.datetime), "Valide que columnas se hayan mapeado a atributos."
        assert isinstance(sender._updated_at, dt.datetime), "Valide que columnas se hayan mapeado a atributos."

    def test_sender_bulk_insertion(self, test_session: Session) -> None:
        """Método que contiene la prueba unitaria para validar la correcta
        inserción masiva de entidades de dominio.
        
        Args:
        ----------
        test_session: Session.
            Sesión de conexión a BD."""

        stmt = """
        INSERT INTO senders (id, status, created_at, updated_at)
        VALUES ("1", "UNVERIFIED", "1996-10-01 16:12:23", "1996-10-01 16:12:23"),
               ("2", "VERIFIED", "2000-12-07 16:12:23", "2018-06-12 13:12:23"),
               ("3", "UNVERIFIED", "2000-12-07 16:12:23", "2018-06-12 13:12:23");
        """

        test_session.execute(text(stmt))

        entities = test_session.query(Sender).order_by(Sender._id).all()

        assert isinstance(entities, list), "Valide que se obtenga una lista de N entidades."
        assert len(entities) == 3, "Valide que la cantidad de entidades obtenidas sea igual a la cantidad de entidades persistidas."
        
        assert isinstance(entities[0], Sender), "Valida que la las entidades tengan el tipado correcto."
        assert isinstance(entities[1], Sender), "Valida que la las entidades tengan el tipado correcto."
        assert isinstance(entities[1], Sender), "Valida que la las entidades tengan el tipado correcto."

        assert entities[0].id.value == "1", "Valida que los valores persistidos si se cargan correctamente a tus entidades."
        assert entities[1].status.value == "VERIFIED", "Valida que los valores persistidos si se cargan correctamente a tus entidades."

    def test_sender_retrieval(self, test_session: Session) -> None:
        """Método que contiene la prueba unitaria para validar la correcta
        extracción de una entidad de dominio.
        
        Args:
        ----------
        test_session: Session.
            Sesión de conexión a BD."""

        sender = Sender.create(id = "321")

        test_session.add(sender)
        test_session.commit()

        stmt = """
        SELECT id, status
        FROM senders
        WHERE id = "321";
        """

        sender_rows = test_session.execute(text(stmt)).one()

        assert sender_rows == ("321", "UNVERIFIED"), "Valida que tus registros de tabla correspondan a tus registros de dominio."

    def test_sender_bulk_retrieval(self, test_session: Session) -> None:
        """Método que contiene la prueba unitaria para validar la correcta
        extracción de varias entidades de dominio.
        
        Args:
        ----------
        test_session: Session.
            Sesión de conexión a BD."""

        sender1 = Sender.create(id = "1")
        sender2 = Sender.create(id = "2")
        sender3 = Sender.create(id = "3")

        test_session.add_all((sender1, sender2, sender3))
        test_session.commit()

        stmt = """
        SELECT id, status
        FROM senders
        ORDER BY id ASC;
        """

        rows = test_session.execute(text(stmt)).all()

        assert len(rows) == 3, "Valida que la cantidad de entidades persistidas corresponda a la cantidad de filas."
        assert rows == [("1", "UNVERIFIED"), ("2", "UNVERIFIED"), ("3", "UNVERIFIED")], "Valide la obtenciónde información de su dominio desde las tablas."

    def test_sender_update(self, test_session: Session) -> None:
        """Método que contiene la prueba unitaria para validar que la actualización
        de una entidad se puede ver reflejada en su persistencia.
        
        Args:
        ----------
        test_session: Session.
            Sesión de conexión a BD."""

        created_sender = Sender(id = "123")

        test_session.add(created_sender)
        test_session.commit()

        retrieved_sender = test_session.get(Sender, "123")

        assert retrieved_sender.status == SenderStatus.UNVERIFIED, "Valide un estado inicial."
        assert created_sender == retrieved_sender, "Valide que los objetos de dominicio persistidos y obtenidos sean iguales."
        
        retrieved_sender.verify()
        test_session.commit()

        stmt = """
        SELECT id, status
        FROM senders
        WHERE id = "123";
        """

        row = test_session.execute(text(stmt)).one()

        assert row == ("123", "VERIFIED"), "Valide que haya habido una actualización de estado."

    def test_sender_deletion(self, test_session: Session) -> None:
        """Método que contiene la prueba unitaria para validar la correcta
        eliminación de una entidad de dominio.
        
        Args:
        ----------
        test_session: Session.
            Sesión de conexión a BD."""

        created_sender = Sender(id = "420")

        test_session.add(created_sender)
        test_session.commit()

        retrieved_sender = test_session.get(Sender, "420")

        assert isinstance(retrieved_sender, Sender), "Valida que se haya obtenido la entidad de dominio."

        test_session.delete(retrieved_sender)
        test_session.commit()

        stmt = """
        SELECT id, status
        FROM senders
        WHERE id = "420";
        """

        row = test_session.execute(text(stmt)).one_or_none()

        assert not row, "Valide que haya habido una eliminación de la entidad.."
