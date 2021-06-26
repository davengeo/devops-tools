from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from devopstoolsdaven.reports.logging_processor import init_logger_processor
from devopstoolsdaven.reports.report import init_report
from devopstoolsdaven.templates.templates import Templates
from devopstoolsdaven.vault.vault_fake import VaultFake
from devopstoolsdaven.vault.vault_little import VaultLittle


class Container(DeclarativeContainer):
    config = providers.Configuration()
    log_processor_service = providers.Resource(init_logger_processor,
                                               config_file=config.logging.config_file,
                                               logger=config.logging.logger,
                                               level=config.logging.level
                                               )
    processors_service = providers.List(
        log_processor_service,
    )
    report_service = providers.Resource(init_report,
                                        attributes=config.cloudevents,
                                        processors=processors_service)
    template_service = providers.Singleton(Templates,
                                           templates_folder=config.templates.templates_folder)
    vault_service = providers.Selector(
        config.vault.implementation,
        json=providers.Singleton(VaultFake,
                                 path_json=config.vault.path_json),
        little=providers.Singleton(VaultLittle,
                                   url=config.vault.url,
                                   env=config.vault.env)
    )
