"""Simulation-based Typical Meteorological Year generator."""

from importlib import metadata as _metadata

__all__ = ["generate_tmy", "FSResult"]

from .fs_rank import fs_rank_month, FSResult
from .selector import generate_tmy
__version__ = _metadata.version(__name__)
