"""Presence Pathways research toolkit."""

from .analysis import add_constructs, analyze_dataset
from .schema import SchemaError, validate_ema
from .synthetic import generate_demo_cohort

__all__ = [
    "SchemaError",
    "add_constructs",
    "analyze_dataset",
    "generate_demo_cohort",
    "validate_ema",
]

__version__ = "0.1.0"
