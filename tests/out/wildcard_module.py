import os
import sys
from importlib.machinery import ModuleSpec, SourceFileLoader


class BundleImporter(SourceFileLoader):
    """Importer that supports importing from strings in code.

    This class is automatically generated by expander.
    """

    module_ispkg = dict()
    module_code = dict()

    @classmethod
    def add_module(cls, fullname, is_package, code):
        cls.module_ispkg[fullname] = is_package
        cls.module_code[cls.get_filename(fullname)] = bytes(code, encoding="utf-8")

    @classmethod
    def find_spec(cls, fullname, path=None, target=None):
        if fullname in cls.module_ispkg:
            return ModuleSpec(
                fullname,
                cls(fullname, ""),
                is_package=cls.module_ispkg[fullname],
            )
        else:
            return None

    @classmethod
    def get_filename(cls, fullname):
        return fullname.replace(".", "_") + ".py"

    def get_data(self, path):
        try:
            return self.module_code[path]
        except KeyError:
            with open(path, "rb") as file:
                return file.read()

    def path_stats(self, path):
        return {"mtime": os.stat(__file__).st_mtime, "size": None}


BundleImporter.add_module(
    fullname="testlib_a",
    is_package=True,
    code="""\
__version__ = "1.0.0"
""",
)

BundleImporter.add_module(
    fullname="testlib_a.sublib_c",
    is_package=True,
    code="""\
from .sub_ca import *
from .sub_cb import *
""",
)

BundleImporter.add_module(
    fullname="testlib_a.sublib_c.sub_ca",
    is_package=False,
    code="""\
__all__ = ("include_def", "include_variable")


def include_def():
    print(__name__)


def exclude_def():
    print(__name__)


_under_score = "under_score"
include_variable = "include_variable"
exclude_variable = "exclude_variable"
""",
)

BundleImporter.add_module(
    fullname="testlib_a.sublib_c.sub_cb",
    is_package=False,
    code="""\
def func():
    print(__name__)


_under_score = "under_score"
variable = "variable"
""",
)

sys.meta_path.append(BundleImporter)

import testlib_a.sublib_c as lib

lib.func()
print(lib.variable)
