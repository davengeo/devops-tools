from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from devopstoolsdaven.common.config import Config
from devopstoolsdaven.reports.report import Report


class Container(DeclarativeContainer):
    config = providers.Configuration()
    config_dependency = providers.Dependency(instance_of=Config)
    report_service = providers.Singleton(Report,
                                         config=config_dependency,
                                         processors=[])
