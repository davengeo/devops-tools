from prometheus_client import REGISTRY


def unregister_metrics() -> None:
    # noinspection PyProtectedMember
    for collector, names in tuple(REGISTRY._collector_to_names.items()):
        REGISTRY.unregister(collector)
