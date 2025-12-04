# Technical Stack

ALWAYS RUN FROM .venv or USING uv

## Build System

- Package manager: `uv` (recommended) or `pip`
- Build backend: `hatchling`
- Python version: 3.11+

## Core Dependencies

- `py-moneyed` (>=3.0) - Industry-standard money handling with Decimal precision
- `babel` (>=2.12.0) - Locale-aware formatting via CLDR
- `requests` (>=2.31.0) - HTTP client with retry logic
- `cryptography` (>=41.0.0) - Fernet encryption for cache
- `platformdirs` (>=4.0.0) - Cross-platform cache directory paths
- `python-Levenshtein` (>=0.21.0) - Fuzzy locale matching

## Development Dependencies

- `pytest` (>=7.4.0) - Testing framework
- `pytest-cov` (>=4.1.0) - Coverage reporting
- `black` (>=23.0.0) - Code formatting
- `ruff` (>=0.1.0) - Linting
- `mypy` (>=1.5.0) - Type checking

## Common Commands

### Installation
```bash
# Using uv (recommended)
uv pip install -e .

# Using pip
pip install -e .

# With dev dependencies
uv pip install -e ".[dev]"
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_config.py -v

# Run stress tests
pytest tests/test_stress.py -v
```

### Code Quality
```bash
# Format code
black .

# Lint code
ruff check .

# Type check
mypy pypenny
```

### Running Demo
```bash
python demo.py
```

## Architecture Patterns

- Configuration-driven behavior via `CurrencyConfig`
- Facade pattern with `CurrencyManager` as main API
- Strategy pattern for exchange rate fetching (live/cached/auto)
- Repository pattern for encrypted cache storage
- Explicit error handling with custom exception hierarchy
