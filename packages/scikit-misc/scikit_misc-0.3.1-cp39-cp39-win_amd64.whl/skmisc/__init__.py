"""""" # start delvewheel patch
def _delvewheel_patch_1_5_1():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'scikit_misc.libs'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-scikit_misc-0.3.1')
        if os.path.isfile(load_order_filepath):
            with open(os.path.join(libs_dir, '.load-order-scikit_misc-0.3.1')) as file:
                load_order = file.read().split()
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if os.path.isfile(lib_path) and not ctypes.windll.kernel32.LoadLibraryExW(ctypes.c_wchar_p(lib_path), None, 0x00000008):
                    raise OSError('Error loading {}; {}'.format(lib, ctypes.FormatError()))


_delvewheel_patch_1_5_1()
del _delvewheel_patch_1_5_1
# end delvewheel patch

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version('scikit_misc')
except PackageNotFoundError:
    # package is not installed
    pass
finally:
    del version
    del PackageNotFoundError

__all__ = ['__version__']

try:
    from skmisc.__config__ import show as show_config  # noqa: F401
except ImportError as err:
    msg = """Error importing skmisc: you cannot import skmisc while
    being in skmisc source directory; please exit the skmisc source
    tree first, and relaunch your python intepreter."""
    raise ImportError('\n\n'.join([err.message, msg]))  # type: ignore
else:
    __all__.append('show_config')


    def test(args=None, plugins=None):
        """
        Run tests
        """
        from pathlib import Path
        # The doctests are not run when called from an installed
        # package since the pytest.ini is not included in the
        # package.
        try:
            import pytest
        except ImportError:
            msg = "To run the tests, you must install pytest"
            raise ImportError(msg)
        path = str(Path(__file__).parent)
        if args is None:
            args = [path]
        else:
            args.append(path)
        return pytest.main(args=args, plugins=plugins)
