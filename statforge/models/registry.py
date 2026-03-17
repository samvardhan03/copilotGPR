from typing import Callable, Type, Dict

class BaseModel:
    def fit(self, data, config):
        raise NotImplementedError

    def effect_size(self) -> dict:
        raise NotImplementedError

MODEL_REGISTRY: Dict[str, Type[BaseModel]] = {}

def register(name: str) -> Callable[[Type[BaseModel]], Type[BaseModel]]:
    """Decorator to register a model class into the StatForge plugin system."""
    def decorator(cls: Type[BaseModel]) -> Type[BaseModel]:
        MODEL_REGISTRY[name] = cls
        return cls
    return decorator
