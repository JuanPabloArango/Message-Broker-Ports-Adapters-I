"""Módulo donde aplicamos el wiring de nuestra app."""

# Librerías Externas.
from typing import Optional

# Librerías Internas.
from app.application.ports.persistence.uow import UnitOfWorkPort

from app.application.query_handlers.get_driver import GetDriverHandler
from app.application.query_handlers.list_drivers import ListDriversHandler
from app.application.command_handlers.free_driver import FreeDriverHandler
from app.application.command_handlers.create_driver import CreateDriverHandler

from app.application.query_handlers.get_sender import GetSenderHandler
from app.application.query_handlers.list_senders import ListSendersHandler
from app.application.command_handlers.create_sender import CreateSenderHandler
from app.application.command_handlers.verify_sender import VerifySenderHandler

from app.application.query_handlers.get_package import GetPackageHandler
from app.application.query_handlers.list_packages import ListPackagesHandler
from app.application.command_handlers.assign_driver import AssignDriverHandler
from app.application.command_handlers.create_package import CreatePackageHandler
from app.application.command_handlers.deliver_package import DeliverPackageHandler

from app.infrastructure.persistence.orm import start_mappers, get_session_factory
from app.infrastructure.persistence.repository.sql.uow import SQLUnitOfWorkAdapter

from app.infrastructure.http.views.driver import DriverView, DriverDetailView, FreeDriverView, blp as DriverBlueprint
from app.infrastructure.http.views.sender import SenderView, SenderDetailView, SenderVerificationView, blp as SenderBlueprint
from app.infrastructure.http.views.package import PackagerView, PackageDetailView, DeliverPackageView, AssignDriverView, blp as PackageBlueprint


def bootstrap(unit_of_work: Optional[UnitOfWorkPort] = None) -> None:
    """Función Facade que implementa el Composition Root donde
    ocurre todo el wiring de nuestra app."""

    if not unit_of_work:
        start_mappers()
        unit_of_work = SQLUnitOfWorkAdapter(session_factory = get_session_factory())

    DriverBlueprint.add_url_rule(rule = "",
                                 view_func = DriverView.as_view(
                                     name = "driver_view",
                                     list_handler = ListDriversHandler(unit_of_work = unit_of_work),
                                     create_handler = CreateDriverHandler(unit_of_work = unit_of_work)
                                 ))
    
    DriverBlueprint.add_url_rule(rule = "/<string:driver_id>",
                                 view_func = DriverDetailView.as_view(
                                     name = "driver_detail_view",
                                     get_handler = GetDriverHandler(unit_of_work = unit_of_work)
                                 ))
    
    DriverBlueprint.add_url_rule(rule = "/<string:driver_id>/free",
                                 view_func = FreeDriverView.as_view(
                                     name = "free_driver_view",
                                     free_handler = FreeDriverHandler(unit_of_work = unit_of_work)
                                 ))

    SenderBlueprint.add_url_rule(rule = "",
                                 view_func = SenderView.as_view(
                                     name = "sender_view",
                                     list_handler = ListSendersHandler(unit_of_work = unit_of_work),
                                     create_handler = CreateSenderHandler(unit_of_work = unit_of_work)))

    SenderBlueprint.add_url_rule(rule = "/<string:sender_id>",
                                 view_func = SenderDetailView.as_view(
                                     name = "sender_detail_view",
                                     get_handler = GetSenderHandler(unit_of_work = unit_of_work)))
    
    SenderBlueprint.add_url_rule(rule = "/<string:sender_id>/verify",
                                 view_func = SenderVerificationView.as_view(
                                     name = "sender_verification_view",
                                     verification_handler = VerifySenderHandler(unit_of_work = unit_of_work)))
    
    PackageBlueprint.add_url_rule(rule = "",
                                  view_func = PackagerView.as_view(
                                      name = "package_view",
                                      list_handler = ListPackagesHandler(unit_of_work = unit_of_work),
                                      create_handler = CreatePackageHandler(unit_of_work = unit_of_work)
                                  ))
    
    PackageBlueprint.add_url_rule(rule = "/<string:package_id>",
                                  view_func = PackageDetailView.as_view(
                                      name = "package_detail_view",
                                      get_handler = GetPackageHandler(unit_of_work = unit_of_work)
                                  ))
    
    PackageBlueprint.add_url_rule(rule = "/<string:package_id>/deliver",
                                  view_func = DeliverPackageView.as_view(
                                      name = "package_deliver_view",
                                      deliver_handler = DeliverPackageHandler(unit_of_work = unit_of_work)
                                  ))
    
    PackageBlueprint.add_url_rule(rule = "/<string:package_id>/assign",
                                  view_func = AssignDriverView.as_view(
                                      name = "package_assignment_view",
                                      assign_handler = AssignDriverHandler(unit_of_work = unit_of_work)
                                  ))
