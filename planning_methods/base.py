import importlib
from abc import ABC, abstractmethod
from copy import deepcopy
from pathlib import Path
from typing import Type, Callable


class BasePlanningMethod(ABC):
    NAME = ''

    @staticmethod
    @abstractmethod
    def sorted_matrix(matrix: list[list[float]], machines: int, details: int) -> list[list[float | int]]:
        ...


def create_extended_matrix(
    matrix: list[list[float]],
) -> list[list[float | int]]:
    extended_matrix = deepcopy(matrix)
    for index, col in enumerate(extended_matrix):
        col.append(index + 1)
        col.append(0)
    return extended_matrix


class StrategyRegistry:
    _strategies: dict[str, Type[BasePlanningMethod]] = dict()

    @classmethod
    def register(cls) -> Callable:
        def wrapper(strategy_class: Type[BasePlanningMethod]) -> Type[BasePlanningMethod]:
            cls._strategies[strategy_class.NAME] = strategy_class
            return strategy_class
        return wrapper

    @classmethod
    def get_strategies(cls) -> dict[str, Type[BasePlanningMethod]]:
        return cls._strategies.copy()

    @classmethod
    def get_strategy(cls, name) -> Type[BasePlanningMethod]:
        return cls._strategies.get(name)

    @classmethod
    def load_strategies(cls, path: str):
        package_dir = Path(path)
        for module_file in package_dir.glob("*.py"):
            if module_file.name in ("__init__.py", "base.py"):
                continue
            module_name = module_file.stem
            importlib.import_module(f"{path}.{module_name}")
