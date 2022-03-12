from __future__ import annotations

from aspy.refactor_imports.import_obj import FromImport
from aspy.refactor_imports.import_obj import ImportImport
from aspy.refactor_imports.sort import sort


IMPORTS = (
    FromImport.from_str('from os import path'),
    FromImport.from_str('from aspy import refactor_imports'),
    ImportImport.from_str('import sys'),
    ImportImport.from_str('import pyramid'),
)


def test_separate_import_before_from():
    ret = sort(IMPORTS)
    assert ret == (
        (
            ImportImport.from_str('import sys'),
            FromImport.from_str('from os import path'),
        ),
        (
            ImportImport.from_str('import pyramid'),
        ),
        (
            FromImport.from_str('from aspy import refactor_imports'),
        ),
    )


def test_future_from_always_first():
    ret = sort(
        (
            FromImport.from_str('from __future__ import absolute_import'),
            ImportImport.from_str('import __future__'),
        ),
    )
    assert ret == (
        (FromImport.from_str('from __future__ import absolute_import'),),
        (ImportImport.from_str('import __future__'),),
    )


def test_passes_through_kwargs_to_classify(in_tmpdir, no_empty_path):
    # Make a module
    in_tmpdir.join('my_module.py').ensure()

    imports = (
        ImportImport.from_str('import my_module'),
        ImportImport.from_str('import pyramid'),
    )
    # Without kwargs, my_module should get classified as application (in a
    # separate group).
    ret = sort(imports)
    assert ret == (
        (ImportImport.from_str('import pyramid'),),
        (ImportImport.from_str('import my_module'),),
    )
    # But when we put the application at a nonexistent directory
    # it'll be third party (and in the same group as pyramid)
    ret = sort(imports, application_directories=('dne',))
    assert ret == (imports,)
