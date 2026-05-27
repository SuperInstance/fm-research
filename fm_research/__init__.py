"""fm-research — Research tools for the Forgemaster system."""

__version__ = "0.1.0"

from .paper import Paper
from .search import ResearchSearch
from .extractor import KeyExtractor
from .synthesizer import Synthesizer
from .catalog import ResearchCatalog

__all__ = ["Paper", "ResearchSearch", "KeyExtractor", "Synthesizer", "ResearchCatalog"]
