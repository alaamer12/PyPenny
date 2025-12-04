# pypenny - Complete Usage Guide

## Table of Contents
1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Configuration](#configuration)
4. [Creating Money Objects](#creating-money-objects)
5. [Arithmetic Operations](#arithmetic-operations)
6. [Currency Conversion](#currency-conversion)
7. [Formatting](#formatting)
8. [Comparison Operations](#comparison-operations)
9. [Immutability](#immutability)
10. [Cache Management](#cache-management)
11. [Error Handling](#error-handling)
12. [Advanced Usage](#advanced-usage)

---

## Installation

```bash
# Using uv (recommended)
uv pip install pypenny

# Using pip
pip install pypenny
```

---

## Quick Start

```python
import pypenny as pp

# Configure once (optional - auto-configures if not called)
pp.config(application_name="MyApp")

# Create money
money = pp.Money('100', 'USD')

# Arithmetic
doubled = money * 2
total = money + pp.Money('50', 'USD')

# Convert currency
egp_money = pp.convert(money, 'EGP')

# Format for display
print(pp.format(egp_money, locale='ar_EG'))
```

---

## Configuration

### Basic Configuration

```python
import pypenny as pp

# Simple configuration
pp.config(application_name="MyApp")
```

### Advanced Configuration

```python
# With all options
pp.config(
    application_name="MyApp",
    allowed_currencies=['USD', 'EGP', 'EUR'],  # Whitelist currencies
    allow_cache_fallback=True,                  # Use cache if network fails
    cache_max_records=10,                       # Max cached rates per pair
    cache_retention_days=7,                     # Days to keep cached rates
    default_exchange_strategy='auto',           # 'live', 'cached', or 'auto'
    default_locale='en_US',                     # Default formatting locale
    api_key=None,                               # Optional API key
    api_timeout=5,                              # API request timeout
    api_max_retries=3                           # Max retry attempts
)
```

### Configuration with Dictionary

```python
config_dict = {
    'application_name': 'MyApp',
    'allowed_currencies': ['USD', 'EGP'],
    'allow_cache_fallback': True
}

pp.config(config_dict=config_dict)
```

### Configuration with Config Object

```python
from pypenny import CurrencyConfig

config = CurrencyConfig(
    application_name="MyApp",
    allowed_currencies=['USD', 'EGP']
)

pp.config(config_obj=config)
```

---

## Creating Money Objects

### From Amount and Currency

```python
import pypenny as pp

# From string
money1 = pp.Money('100.50', 'USD')

# From integer
money2 = pp.Money(100, 'USD')

# From float (not recommended due to precision)
money3 = pp.Money(100.50, 'USD')

# From Decimal (recommended for precision)
from decimal import Decimal
money4 = pp.Money(Decimal('100.50'), 'USD')
```

### From Another Money Instance

```python
# Create a copy with different frozen state
frozen_money = pp.Money('100', 'USD')  # Frozen by default
unfrozen_copy = pp.Money(frozen_money, frozen=False)

# Create frozen copy from unfrozen
mutable_money = pp.Money('100', 'USD', frozen=False)
immutable_copy = pp.Money(mutable_money, frozen=True)
```

### Zero Money

```python
# Create zero money in a currency
zero_usd = pp.Money.zero('USD')
zero_egp = pp.Money.zero('EGP', frozen=False)
```

### Using create_money Function

```python
# Alternative functional API
money = pp.create_money('100', 'USD')
```

---

## Arithmetic Operations

### Addition

```python
money1 = pp.Money('100', 'USD')
money2 = pp.Money('50', 'USD')

# Using dunder method
total = money1 + money2  # USD 150

# Using functional API
total = pp.add(money1, money2)

# Using sum() with multiple Money objects
items = [
    pp.Money('10', 'USD'),
    pp.Money('20', 'USD'),
    pp.Money('30', 'USD')
]
total = sum(items, pp.Money.zero('USD'))  # USD 60
```

### Subtraction

```python
money1 = pp.Money('100', 'USD')
money2 = pp.Money('30', 'USD')

# Using dunder method
difference = money1 - money2  # USD 70

# Using functional API
difference = pp.subtract(money1, money2)
```

### Multiplication

```python
money = pp.Money('50', 'USD')

# Using dunder method
doubled = money * 2        # USD 100
tripled = 3 * money        # USD 150 (right-hand multiplication)

# Using functional API
doubled = pp.multiply(money, 2)

# With Decimal for precision
from decimal import Decimal
result = money * Decimal('1.5')  # USD 75
```

### Division

```python
money = pp.Money('100', 'USD')

# Using dunder method
half = money / 2           # USD 50
third = money / 3          # USD 33.33...

# Using functional API
half = pp.divide(money, 2)
```

### Floor Division

```python
money = pp.Money('100', 'USD')

# Using dunder method
result = money // 3        # USD 33

# Using functional API
result = pp.floor_divide(money, 3)
```

### Power

```python
money = pp.Money('10', 'USD')

# Using dunder method
squared = money ** 2       # USD 100
cubed = money ** 3         # USD 1000

# Using functional API
squared = pp.power(money, 2)
```

### Unary Operations

```python
money = pp.Money('100', 'USD')

# Negation
negative = -money          # USD -100

# Positive (no-op)
positive = +money          # USD 100

# Absolute value
abs_value = abs(pp.Money('-50', 'USD'))  # USD 50
```

---

## Currency Conversion

### Basic Conversion

```python
import pypenny as pp

pp.config(application_name="MyApp")

# Create money in USD
usd_money = pp.Money('100', 'USD')

# Convert to EGP
egp_money = pp.convert(usd_money, 'EGP')
print(pp.format(egp_money))  # e.g., "EGP 4,757.00"
```

### Conversion Strategies

```python
# Live conversion (always fetch from network)
egp_money = pp.convert(usd_money, 'EGP', strategy='live')

# Cached conversion (use local cache only)
egp_money = pp.convert(usd_money, 'EGP', strategy='cached')

# Auto conversion (try live, fallback to cache)
egp_money = pp.convert(usd_money, 'EGP', strategy='auto')  # Default
```

### Handling Conversion Errors

```python
try:
    converted = pp.convert(money, 'EGP')
except pp.ExchangeRateUnavailableError as e:
    print(f"Cannot convert: {e}")
    # Use cached rate or handle error
except pp.ConversionError as e:
    print(f"Conversion failed: {e}")
```

---

## Formatting

### Basic Formatting

```python
import pypenny as pp

money = pp.Money('100.50', 'USD')

# Format with default locale
formatted = pp.format(money)  # "$100.50"

# Format with specific locale
us_format = pp.format(money, locale='en_US')    # "$100.50"
fr_format = pp.format(money, locale='fr_FR')    # "100,50 $US"
de_format = pp.format(money, locale='de_DE')    # "100,50 $"
ar_format = pp.format(money, locale='ar_EG')    # Different format
```

### Fuzzy Locale Matching

pypenny automatically corrects common locale mistakes:

```python
money = pp.Money('100', 'USD')

# All of these work (auto-corrected to 'en_US')
pp.format(money, locale='EN_us')    # Mixed case
pp.format(money, locale='US_EN')    # Swapped order
pp.format(money, locale='em_US')    # Typo (corrected)
pp.format(money, locale='US')       # Alias
```

### Custom Formatting Options

```python
# Pass additional Babel formatting options
formatted = pp.format(
    money,
    locale='en_US',
    pattern='¤#,##0.00',  # Custom pattern
    currency_digits=False  # Don't use currency-specific digits
)
```

---

## Comparison Operations

### Basic Comparisons

```python
money1 = pp.Money('100', 'USD')
money2 = pp.Money('50', 'USD')
money3 = pp.Money('100', 'USD')

# All comparison operators work (via @total_ordering)
print(money1 > money2)   # True
print(money1 < money2)   # False
print(money1 >= money3)  # True
print(money1 <= money3)  # True
print(money1 == money3)  # True
print(money1 != money2)  # True
```

### Sorting

```python
money_list = [
    pp.Money('50', 'USD'),
    pp.Money('100', 'USD'),
    pp.Money('25', 'USD')
]

# Sort ascending
sorted_list = sorted(money_list)  # [25, 50, 100]

# Sort descending
sorted_desc = sorted(money_list, reverse=True)  # [100, 50, 25]
```

### Using in Sets and Dicts

```python
# Money objects are hashable
money_set = {
    pp.Money('100', 'USD'),
    pp.Money('100', 'USD'),  # Duplicate, will be removed
    pp.Money('50', 'USD')
}
print(len(money_set))  # 2

# Use as dictionary keys
prices = {
    pp.Money('10', 'USD'): 'Small',
    pp.Money('20', 'USD'): 'Medium',
    pp.Money('30', 'USD'): 'Large'
}
```

### Currency Mismatch in Comparisons

```python
usd = pp.Money('100', 'USD')
egp = pp.Money('1000', 'EGP')

try:
    result = usd > egp  # Error!
except pp.CurrencyMismatchError as e:
    print(f"Cannot compare: {e}")
    # Convert to same currency first
    egp_as_usd = pp.convert(egp, 'USD')
    result = usd > egp_as_usd  # Now works
```

---

## Immutability

### Frozen Money (Default)

```python
# Money objects are immutable by default
money = pp.Money('100', 'USD')

print(money.is_frozen)  # True

# Attempting to modify raises error
try:
    money.amount = 200
except AttributeError as e:
    print(f"Cannot modify: {e}")
```

### Mutable Money

```python
# Create mutable money
mutable_money = pp.Money('100', 'USD', frozen=False)

print(mutable_money.is_frozen)  # False

# Note: Even mutable Money objects should not be modified directly
# Always create new Money objects through operations
```

### Converting Between Frozen States

```python
# Create frozen copy from unfrozen
mutable = pp.Money('100', 'USD', frozen=False)
immutable = pp.Money(mutable, frozen=True)

# Create unfrozen copy from frozen
frozen = pp.Money('100', 'USD')
unfrozen = pp.Money(frozen, frozen=False)
```

### Why Immutability?

```python
# Immutability prevents bugs
original = pp.Money('100', 'USD')
prices = [original, original, original]

# If Money were mutable, modifying one would affect all
# But with immutability, each operation creates a new object
new_price = original * 2  # Creates new Money, original unchanged
```

---

## Cache Management

### Get Cache Statistics

```python
import pypenny as pp

# Get cache stats
stats = pp.get_cache_stats()

print(f"Total records: {stats['total_records']}")
print(f"Currency pairs: {stats['currency_pairs']}")
print(f"Cache file: {stats['cache_file']}")
```

### Cleanup Old Records

```python
# Remove records older than retention period
removed_count = pp.cleanup_cache()
print(f"Removed {removed_count} old records")
```

### Clear All Cache

```python
# Clear all cached exchange rates
pp.clear_cache()
```

### Cache Configuration

```python
# Configure cache behavior
pp.config(
    application_name="MyApp",
    cache_max_records=10,        # Max records per currency pair
    cache_retention_days=7,      # Days to keep records
    allow_cache_fallback=True    # Use cache if network fails
)
```

### Cache Location

Cache files are stored in platform-specific directories:
- **Windows**: `C:\Users\<user>\AppData\Local\<app_name>\Cache\exchange_cache.enc`
- **Linux**: `~/.cache/<app_name>/exchange_cache.enc`
- **macOS**: `~/Library/Caches/<app_name>/exchange_cache.enc`

---

## Error Handling

### Exception Hierarchy

```python
import pypenny as pp

# Base exception
pp.CurrencyException

# Configuration errors
pp.ConfigurationError

# Currency validation errors
pp.InvalidCurrencyCodeError
pp.CurrencyNotAllowedError

# Locale errors
pp.InvalidLocaleError

# Conversion errors
pp.ExchangeRateUnavailableError
pp.CurrencyMismatchError
pp.ConversionError

# Cache errors
pp.CacheError
pp.EncryptionError
```

### Handling Specific Errors

```python
import pypenny as pp

pp.config(
    application_name="MyApp",
    allowed_currencies=['USD', 'EGP']
)

# Invalid currency code
try:
    money = pp.Money('100', 'USDD')  # Typo
except pp.InvalidCurrencyCodeError as e:
    print(f"Error: {e}")
    # Error includes suggestions: "Did you mean: USD?"

# Currency not allowed
try:
    money = pp.Money('100', 'EUR')  # Not in whitelist
except pp.CurrencyNotAllowedError as e:
    print(f"Error: {e}")
    # Error: Currency 'EUR' not allowed. Allowed: USD, EGP

# Currency mismatch in operations
try:
    usd = pp.Money('100', 'USD')
    egp = pp.Money('1000', 'EGP')
    total = usd + egp  # Different currencies
except pp.CurrencyMismatchError as e:
    print(f"Error: {e}")
    # Error: Cannot perform addition on different currencies

# Conversion errors
try:
    converted = pp.convert(money, 'EGP')
except pp.ExchangeRateUnavailableError as e:
    print(f"Rate unavailable: {e}")
except pp.ConversionError as e:
    print(f"Conversion failed: {e}")
```

### Helpful Error Messages

pypenny provides detailed error messages with suggestions:

```python
# Invalid currency with suggestions
try:
    money = pp.Money('100', 'USDD')
except pp.InvalidCurrencyCodeError as e:
    print(e)
    # "Invalid currency code: 'USDD'. Did you mean: USD?"

# Invalid locale with suggestions
try:
    pp.format(money, locale='invalid')
except pp.InvalidLocaleError as e:
    print(e)
    # "Invalid locale: 'invalid'. Did you mean: en_US, en_GB?"
```

---

## Advanced Usage

### Working with CurrencyManager Directly

```python
from pypenny import CurrencyConfig, CurrencyManager

# Create custom configuration
config = CurrencyConfig(
    application_name="AdvancedApp",
    allowed_currencies=['USD', 'EGP', 'EUR']
)

# Create manager
manager = CurrencyManager(config)

# Use manager methods
money = manager.create_money('100', 'USD')
converted = manager.convert(money.get_moneyed_object(), 'EGP')
formatted = manager.format(converted, locale='ar_EG')
```

### Custom Exchange Rate Provider

```python
from pypenny._core import ExchangeRateService, ExchangeRateProvider

# Create custom exchange service
exchange_service = ExchangeRateService(
    provider=ExchangeRateProvider.EXCHANGERATE_API,
    api_key='your_api_key',
    cache_duration_minutes=120,  # Cache for 2 hours
    timeout=10,
    max_retries=5
)
```

### Database Serialization

```python
from pypenny._core import MoneySerializer

money = pp.Money('100.50', 'USD').get_moneyed_object()

# Serialize for database
db_data = MoneySerializer.to_dict(money)
# {
#     'amount': '100.50',
#     'amount_sub_units': 10050,
#     'currency': 'USD',
#     'currency_name': 'US Dollar',
#     'timestamp': '2025-12-04T...'
# }

# Deserialize from database
money_from_db = MoneySerializer.from_dict(db_data)

# Create from sub-units (cents/piasters)
money_from_cents = MoneySerializer.from_sub_units(10050, 'USD')  # $100.50
```

### Batch Operations

```python
# Process multiple conversions
amounts = [100, 200, 300]
currencies = ['USD', 'EUR', 'GBP']

money_objects = [pp.Money(amt, curr) for amt, curr in zip(amounts, currencies)]

# Convert all to EGP
egp_amounts = []
for money in money_objects:
    try:
        converted = pp.convert(money, 'EGP')
        egp_amounts.append(converted)
    except pp.ConversionError:
        continue
```

### Type Checking with mypy

```python
from typing import List
import pypenny as pp

def calculate_total(items: List[pp.Money]) -> pp.Money:
    """Calculate total of money items (all same currency)"""
    if not items:
        raise ValueError("Items list cannot be empty")
    
    currency = items[0].currency_code
    return sum(items, pp.Money.zero(currency))

# mypy will catch type errors
items: List[pp.Money] = [
    pp.Money('10', 'USD'),
    pp.Money('20', 'USD')
]
total: pp.Money = calculate_total(items)
```

---

## Best Practices

### 1. Always Use Decimal for Precision

```python
from decimal import Decimal

# Good
money = pp.Money(Decimal('100.50'), 'USD')

# Acceptable
money = pp.Money('100.50', 'USD')

# Avoid (floating point precision issues)
money = pp.Money(100.50, 'USD')
```

### 2. Configure Once at Application Start

```python
# In your app initialization
def init_app():
    pp.config(
        application_name="MyApp",
        allowed_currencies=['USD', 'EGP', 'EUR'],
        allow_cache_fallback=True
    )

# Then use throughout your app
def process_payment(amount: str, currency: str):
    money = pp.Money(amount, currency)
    # ... rest of logic
```

### 3. Use Immutable Money by Default

```python
# Default (immutable) - prevents bugs
money = pp.Money('100', 'USD')

# Only use mutable if you have a specific reason
mutable_money = pp.Money('100', 'USD', frozen=False)
```

### 4. Handle Currency Mismatches Explicitly

```python
def add_prices(price1: pp.Money, price2: pp.Money) -> pp.Money:
    """Add two prices, converting if necessary"""
    if price1.currency_code != price2.currency_code:
        # Convert price2 to price1's currency
        price2 = pp.convert(price2, price1.currency_code)
    
    return price1 + price2
```

### 5. Use Appropriate Formatting

```python
# For display to users
display_text = pp.format(money, locale='en_US')

# For logging/debugging
log_text = str(money)  # "USD 100"
debug_text = repr(money)  # "Money('100', 'USD')"
```

---

## Complete Example Application

```python
"""
E-commerce shopping cart with multi-currency support
"""

import pypenny as pp
from typing import List, Dict
from decimal import Decimal

# Initialize pypenny
pp.config(
    application_name="EcommerceApp",
    allowed_currencies=['USD', 'EUR', 'GBP', 'EGP'],
    allow_cache_fallback=True,
    cache_retention_days=1
)

class ShoppingCart:
    def __init__(self, currency: str = 'USD'):
        self.currency = currency
        self.items: List[pp.Money] = []
    
    def add_item(self, price: pp.Money):
        """Add item to cart, converting currency if needed"""
        if price.currency_code != self.currency:
            price = pp.convert(price, self.currency)
        self.items.append(price)
    
    def get_total(self) -> pp.Money:
        """Calculate cart total"""
        if not self.items:
            return pp.Money.zero(self.currency)
        return sum(self.items, pp.Money.zero(self.currency))
    
    def apply_discount(self, percent: Decimal) -> pp.Money:
        """Apply percentage discount"""
        total = self.get_total()
        discount_amount = total * (percent / 100)
        return total - discount_amount
    
    def format_total(self, locale: str = 'en_US') -> str:
        """Format total for display"""
        return pp.format(self.get_total(), locale=locale)

# Usage
cart = ShoppingCart(currency='USD')

# Add items in different currencies
cart.add_item(pp.Money('29.99', 'USD'))
cart.add_item(pp.Money('25.00', 'EUR'))  # Auto-converted to USD
cart.add_item(pp.Money('19.99', 'GBP'))  # Auto-converted to USD

# Calculate total
total = cart.get_total()
print(f"Cart total: {cart.format_total()}")

# Apply 10% discount
discounted = cart.apply_discount(Decimal('10'))
print(f"After 10% discount: {pp.format(discounted)}")

# Show in different locales
print(f"US format: {pp.format(discounted, locale='en_US')}")
print(f"EU format: {pp.format(discounted, locale='de_DE')}")
print(f"UK format: {pp.format(discounted, locale='en_GB')}")
```

---

## Testing

### Running Tests

```bash
# Run all tests (excluding CI-only)
pytest -v -m "not ci_only"

# Run specific test file
pytest tests/test_config.py -v

# Run with coverage
pytest --cov=pypenny --cov-report=html

# Run CI-only tests
pytest -v -m "ci_only"
```

### Writing Tests with pypenny

```python
import pytest
import pypenny as pp

def test_money_arithmetic():
    """Test money arithmetic operations"""
    money1 = pp.Money('100', 'USD')
    money2 = pp.Money('50', 'USD')
    
    assert money1 + money2 == pp.Money('150', 'USD')
    assert money1 - money2 == pp.Money('50', 'USD')
    assert money1 * 2 == pp.Money('200', 'USD')
    assert money1 / 2 == pp.Money('50', 'USD')

def test_currency_mismatch():
    """Test that currency mismatch raises error"""
    usd = pp.Money('100', 'USD')
    egp = pp.Money('1000', 'EGP')
    
    with pytest.raises(pp.CurrencyMismatchError):
        result = usd + egp
```

---

## Support and Resources

- **Documentation**: This file
- **Demo Files**: 
  - `demo.py` - Comprehensive feature demo
  - `demo_unified_api.py` - Unified API demo
  - `test_money_features.py` - Money class features
- **Source Code**: Check the `pypenny/` directory
- **Tests**: Check the `tests/` directory

---

## License

MIT License - See LICENSE file for details
