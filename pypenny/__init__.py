"""
Robust Currency Conversion Solution

Production-grade currency conversion with smart error handling,
encrypted caching, and fuzzy locale matching.
"""

__version__ = "1.0.0"

from .config import CurrencyConfig
from .currency_manager import CurrencyManager
from .exceptions import (
    CurrencyException,
    ConfigurationError,
    InvalidCurrencyCodeError,
    CurrencyNotAllowedError,
    InvalidLocaleError,
    ExchangeRateUnavailableError,
    CurrencyMismatchError,
    ConversionError,
    CacheError,
    EncryptionError,
)

__all__ = [
    "CurrencyConfig",
    "CurrencyManager",
    "CurrencyException",
    "ConfigurationError",
    "InvalidCurrencyCodeError",
    "CurrencyNotAllowedError",
    "InvalidLocaleError",
    "ExchangeRateUnavailableError",
    "CurrencyMismatchError",
    "ConversionError",
    "CacheError",
    "EncryptionError",
]
