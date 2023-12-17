import sys
import dan.logging
import dan.core.include
from dan.core import asyncio
from dan.core.include import include, requires
from dan.core.generator import generator
from dan.core.target import Target
from dan.pkgconfig.package import find_package


self : dan.core.include.MakeFile

class __LazySelf(sys.__class__):
    @property
    def self(__):
        return dan.core.include.context.current

sys.modules[__name__].__class__ = __LazySelf
