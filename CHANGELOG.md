# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-12-08

### Added
- **Unified API**: Created simple, intuitive package-level API (`pypenny.config`, `pypenny.convert`, etc.).
- **Enhanced Money Class**: New `pypenny.Money` class with immutability, dunder methods for arithmetic, total ordering, and hashability.
- **Arithmetic Operations**: Added comprehensive arithmetic methods (`multiply`, `divide`, `floor_divide`, `power`) to `CurrencyManager` and `Money` class.
- **Test Markers**: Added custom pytest markers (`slow`, `ci_only`) in `pyproject.toml`.

### Fixed
- **Currency Conversion**: Fixed decimal precision error when converting currencies by properly calculating decimal places using `log10(sub_unit)`.
- **Package Configuration**: Fixed package name mismatch in `pyproject.toml` (was `pypillars`, now `pypenny`).
- **Test Imports**: Updated all test imports to use `pypenny.` prefix.
- **Deduplication Logic**: Fixed deduplication test expectations.

### Changed
- **Documentation**: Updated README.md to reflect the new unified API and architecture.
- **Testing**: Marked long-running tests with `@pytest.mark.ci_only`.
