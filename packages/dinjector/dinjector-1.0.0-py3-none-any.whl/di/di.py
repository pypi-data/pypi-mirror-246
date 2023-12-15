"""Implement dependency injections between beams of application.

Simplify the construction of applications.
"""
import abc
import importlib
from dataclasses import dataclass
from typing import Any

import yaml


class ConfigService(abc.ABC):
    def __getitem__(self, key: str) -> Any:
        return self.get(key)

    def __contains__(self, key: str) -> bool:
        return self.get(key) is not None

    @abc.abstractmethod
    def get(self, key: str) -> Any:
        ...


@dataclass(frozen=True)
class BeamDefinition:
    module_name: str
    class_name: str
    args: str | list = ""
    kwargs: str | dict[str, Any] = ""

    def import_class(self, module_base: str = ""):
        module_name = (
            f"{module_base}.{self.module_name}" if module_base else self.module_name
        )
        module = importlib.import_module(module_name)
        return getattr(module, self.class_name)

    @classmethod
    def from_dict(cls, value):
        return cls(
            value["module"],
            value["class"],
            value.get("args", []),
            value.get("kwargs", {}),
        )


class DependencyInjector:
    """Assure the correct injection of beam components to construct all application."""

    def __init__(
        self,
        config_service: ConfigService,
        dependencies_fn: str,
        module_base: str = "",
    ):
        self._config = config_service
        self._base = module_base
        self._beams = {}
        with open(dependencies_fn, "r") as f:
            self._dependencies = yaml.load(f, Loader=yaml.FullLoader)

    def construct(self, beam_name):
        """Create object by its beam name."""
        if beam_name not in self._beams:
            beam_dict = self._dependencies[beam_name]
            definition = BeamDefinition.from_dict(beam_dict)
            Class = definition.import_class(self._base)
            args = []
            def_args = definition.args
            if def_args:
                if type(def_args) is str:
                    def_args = self._config[def_args]

                for arg in def_args:
                    if arg[0] == ">":
                        args.append(self.construct(arg[1:]))
                    else:
                        args.append(self._config[arg])

            kwargs = {}
            def_kwargs = definition.kwargs
            if def_kwargs:
                if type(def_kwargs) is str:
                    kwargs = self._config[def_kwargs]
                elif type(def_kwargs) is dict:
                    for key, value in def_kwargs.items():
                        if value[0] == ">":
                            value_ = self.construct(value[1:])
                        else:
                            value_ = (
                                self._config[value] if value in self._config else value
                            )
                        kwargs[key] = value_
                else:
                    raise ValueError(f"{def_kwargs} can not be processed")

            self._beams[beam_name] = Class(*args, **kwargs)

        return self._beams[beam_name]
