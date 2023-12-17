"""""" # start delvewheel patch
def _delvewheel_patch_1_5_1():
    import os
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'hictkpy.libs'))
    if os.path.isdir(libs_dir):
        os.add_dll_directory(libs_dir)


_delvewheel_patch_1_5_1()
del _delvewheel_patch_1_5_1
# end delvewheel patch

from .hictkpy import File, PixelSelector, is_cooler, is_hic, __hictk_version__
from .hictkpy import cooler

try:
    from importlib.metadata import version
except ModuleNotFoundError:
    from importlib_metadata import version

__version__ = version("hictkpy")
