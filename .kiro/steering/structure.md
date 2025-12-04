# Project Structure

ALWAYS RUN FROM .venv or USING uv

## Directory Layout

```
pypenny/
├── pypenny/              # Main package
│   ├── __init__.py      # Public API exports
│   ├── _core.py         # Core currency logic (py-moneyed integration)
│   ├── config.py        # Configuration class
│   ├── currency_manager.py  # Main user-facing API
│   ├── encryption_utils.py  # Fernet encryption utilities
│   ├── exceptions.py    # Custom exception hierarchy
│   ├── exchange_cache.py    # Encrypted cache management
│   └── locale_matcher.py    # Fuzzy locale normalization
├── tests/               # Test suite
│   ├── conftest.py      # Pytest fixtures
│   ├── test_*.py        # Test modules
│   └── test_stress.py   # Performance/stress tests
├── demo.py              # Comprehensive usage examples
├── pyproject.toml       # Project metadata and dependencies
├── requirements.txt     # Pinned dependencies
└── README.md            # Documentation
```

## Module Responsibilities

### `config.py`
Configuration class with validation for:
- Application settings (name, locale)
- Cache behavior (fallback, retention, max records)
- Currency restrictions (allowed currencies whitelist)
- Exchange strategies (live/cached/auto)
- API settings (key, timeout, retries)

### `currency_manager.py`
Main user-facing API providing:
- `create_money()` - Create Money objects with validation
- `convert()` - Currency conversion with strategy selection
- `format()` - Locale-aware formatting with fuzzy matching
- `add()` / `subtract()` - Safe arithmetic operations
- Cache management methods

### `_core.py`
Low-level currency operations:
- `ExchangeRateService` - Fetches rates from APIs with retry logic
- `CurrencyConverter` - Converts Money objects using exchange rates
- `MoneySerializer` - Database serialization helpers
- `MoneyFormatter` - Locale-aware formatting

### `exchange_cache.py`
Encrypted cache management:
- Stores exchange rates with deduplication
- Fernet encryption for security
- Cross-platform cache directory via platformdirs
- Cleanup of old records based on retention policy

### `locale_matcher.py`
Fuzzy locale matching:
- Normalizes locale codes (case, order)
- Handles common typos via Levenshtein distance
- Resolves country code aliases (US → en_US)

### `exceptions.py`
Custom exception hierarchy:
- `CurrencyException` - Base exception
- `InvalidCurrencyCodeError` - Invalid currency with suggestions
- `CurrencyNotAllowedError` - Currency not in whitelist
- `ExchangeRateUnavailableError` - Network/cache failure
- `CurrencyMismatchError` - Operation on different currencies
- All exceptions provide helpful error messages

## Testing Structure

- `conftest.py` - Shared fixtures (configs, sample data)
- `test_config.py` - Configuration validation tests
- `test_encryption.py` - Encryption utilities tests
- `test_exchange_cache.py` - Cache operations tests
- `test_locale_matcher.py` - Fuzzy matching tests
- `test_stress.py` - Performance and edge case tests

## Naming Conventions

- Classes: PascalCase (e.g., `CurrencyManager`)
- Functions/methods: snake_case (e.g., `create_money`)
- Constants: UPPER_SNAKE_CASE (e.g., `DEFAULT_LOCALE`)
- Private methods: Leading underscore (e.g., `_validate_currency`)
- Test classes: `Test` prefix (e.g., `TestCurrencyConfig`)
- Test functions: `test_` prefix (e.g., `test_requires_application_name`)
