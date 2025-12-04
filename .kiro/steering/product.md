# Product Overview

ALWAYS RUN FROM .venv or USING uv

pypenny is a production-grade Python library for currency conversion with smart error handling, encrypted caching, and fuzzy locale matching.

## Core Value Proposition

Provides developers with a robust, safe currency handling solution that prevents common pitfalls like floating-point errors, string conversion crashes, and network failures.

## Key Features

- Safe string operations - no crashes with `str()` or `print()`
- Fuzzy locale matching - auto-corrects typos (e.g., `em_US` → `en_US`)
- Encrypted cache with AES-128 Fernet encryption
- Deduplication logic - only 1 record per day if rate unchanged
- Supports 180+ ISO 4217 currencies via py-moneyed
- Dual exchange strategies: live network + encrypted local cache fallback
- Flexible configuration for strict or permissive currency handling

## Target Users

Developers building financial applications, e-commerce platforms, or any system requiring reliable multi-currency support with production-grade error handling.
