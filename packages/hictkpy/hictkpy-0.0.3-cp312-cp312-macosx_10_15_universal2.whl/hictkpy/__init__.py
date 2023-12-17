
from .hictkpy import File, PixelSelector, is_cooler, is_hic, __hictk_version__
from .hictkpy import cooler

try:
    from importlib.metadata import version
except ModuleNotFoundError:
    from importlib_metadata import version

__version__ = version("hictkpy")
