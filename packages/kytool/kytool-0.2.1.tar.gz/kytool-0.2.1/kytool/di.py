import inspect
from typing import Any, Callable


class Injector:
    def __init__(self, handler: Callable, dependencies: dict[str, Any]):
        self.handler = handler
        self.dependencies = dependencies

    def __call__(self, message: Any) -> Any:
        return self.handler(message, **self.dependencies)


def inject_dependencies(handler: Callable, dependencies: dict[str, Any]) -> Callable:
    """
    Inject dependencies into a handler function.

    Args:
        handler (Callable): Handler function to inject dependencies into.
        dependencies (dict[str, Any]): Dependencies to inject into the handler.

    Returns:
        Callable: Handler function with dependencies injected.
    """

    params = inspect.signature(handler).parameters
    deps = {
        name: dependency for name, dependency in dependencies.items() if name in params
    }
    return Injector(handler=handler, dependencies=deps)
