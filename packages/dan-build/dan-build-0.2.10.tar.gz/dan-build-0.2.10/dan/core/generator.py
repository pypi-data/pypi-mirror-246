from dan.core.pathlib import Path
from dan.core import asyncio
from dan.core.target import Target, TargetDependencyLike
from typing import Callable
import inspect


class generator:
    def __init__(self, output: str, dependencies: TargetDependencyLike = None, options: dict = None):
        self.output = Path(output)
        self.dependencies = list() if dependencies is None else dependencies
        self.options = dict() if options is None else options

    def __call__(self, fn: Callable):
        class Generator(Target):
            name = self.output.stem
            output = self.output
            dependencies = set(self.dependencies)
            options = self.options

            def __build__(self):
                arg_spec = inspect.getfullargspec(fn)
                if 'self' in arg_spec.args:
                    return fn(self)
                elif not arg_spec.args:
                    return fn()
                else:
                    raise RuntimeError(
                        "Only 'self' is allowed as Generator argument")

        # hack the module location (used for Makefile's Targets resolution)
        Generator.__module__ = fn.__module__
        return Generator
