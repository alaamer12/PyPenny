"""
Demonstration of Robust Currency Conversion Solution

Shows all features:
1. Configuration setup (strict vs. permissive)
2. Creating money with fuzzy locale matching
3. Safe operations (no str() errors)
4. Currency conversion with both strategies
5. Allowed currencies enforcement
6. Cache fallback behavior
7. Error handling with helpful messages
8. Cache inspection and management
"""

from decimal import Decimal
from config import CurrencyConfig
from currency_manager import CurrencyManager
from exceptions import (
    CurrencyNotAllowedError,
    InvalidLocaleError,
    ExchangeRateUnavailableError
)


def print_section(title: str):
    """Print section header"""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)


def demo_basic_usage():
    """Demo 1: Basic usage with permissive config"""
    print_section("1. Basic Usage (Permissive Configuration)")
    
    # Create permissive configuration
    config = CurrencyConfig(
        application_name="DemoApp",
        allow_cache_fallback=True,
        allowed_currencies=None  # All currencies allowed
    )
    
    manager = CurrencyManager(config)
    
    # Create money
    money_usd = manager.create_money('100.50', 'USD')
    money_egp = manager.create_money('1500', 'EGP')
    
    # Format with different locales
    print(f"USD Money: {manager.format(money_usd, locale='en_US')}")
    print(f"EGP Money: {manager.format(money_egp, locale='ar_EG')}")
    
    # Safe operations
    total_usd = manager.add(
        manager.create_money('50', 'USD'),
        manager.create_money('25.50', 'USD')
    )
    print(f"Addition: {manager.format(total_usd, locale='en_US')}")


def demo_fuzzy_locale_matching():
    """Demo 2: Fuzzy locale matching"""
    print_section("2. Fuzzy Locale Matching")
    
    config = CurrencyConfig(application_name="DemoApp")
    manager = CurrencyManager(config)
    
    money = manager.create_money('100', 'USD')
    
    # Test various locale inputs
    test_locales = [
        ('en_US', 'Correct locale'),
        ('EN_us', 'Mixed case'),
        ('US_EN', 'Swapped order'),
        ('US', 'Alias'),
    ]
    
    for locale_input, description in test_locales:
        try:
            formatted = manager.format(money, locale=locale_input)
            print(f"  {description:20} ({locale_input:10}) → {formatted}")
        except InvalidLocaleError as e:
            print(f"  {description:20} ({locale_input:10}) → ERROR: {e}")


def demo_strict_configuration():
    """Demo 3: Strict configuration with allowed currencies"""
    print_section("3. Strict Configuration (USD & EGP only)")
    
    # Create strict configuration
    config = CurrencyConfig(
        application_name="StrictApp",
        allow_cache_fallback=False,  # Fail fast on network errors
        allowed_currencies=['USD', 'EGP']  # Only these two
    )
    
    manager = CurrencyManager(config)
    
    # This works
    money_usd = manager.create_money('100', 'USD')
    print(f"✓ Created USD money: {manager.format(money_usd)}")
    
    money_egp = manager.create_money('1000', 'EGP')
    print(f"✓ Created EGP money: {manager.format(money_egp)}")
    
    # This fails
    try:
        money_eur = manager.create_money('100', 'EUR')
    except CurrencyNotAllowedError as e:
        print(f"\n✗ Tried to create EUR money:")
        print(f"  Error: {e}")


def demo_currency_conversion():
    """Demo 4: Currency conversion with strategies"""
    print_section("4. Currency Conversion")
    
    config = CurrencyConfig(
        application_name="ConversionDemo",
        allow_cache_fallback=True
    )
    
    manager = CurrencyManager(config)
    
    money_usd = manager.create_money('100', 'USD')
    print(f"Original: {manager.format(money_usd, locale='en_US')}")
    
    try:
        # Convert USD to EGP
        money_egp = manager.convert(money_usd, 'EGP', strategy='auto')
        print(f"Converted to EGP: {manager.format(money_egp, locale='ar_EG')}")
        
        # Convert back
        money_usd_back = manager.convert(money_egp, 'USD', strategy='auto')
        print(f"Converted back to USD: {manager.format(money_usd_back, locale='en_US')}")
        
    except Exception as e:
        print(f"Conversion failed: {e}")
        print("(This is expected if no network connection)")


def demo_cache_management():
    """Demo 5: Cache management"""
    print_section("5. Cache Management")
    
    config = CurrencyConfig(
        application_name="CacheDemo",
        cache_max_records=5,
        cache_retention_days=3
    )
    
    manager = CurrencyManager(config)
    
    # Get cache stats
    stats = manager.get_cache_stats()
    print(f"Cache Statistics:")
    print(f"  Total records: {stats['total_records']}")
    print(f"  Currency pairs: {stats['currency_pairs']}")
    print(f"  Cache file: {stats['cache_file']}")
    
    # Try conversion to populate cache
    try:
        money = manager.create_money('100', 'USD')
        converted = manager.convert(money, 'EGP')
        
        # Check stats again
        stats = manager.get_cache_stats()
        print(f"\nAfter conversion:")
        print(f"  Total records: {stats['total_records']}")
        print(f"  Currency pairs: {stats['currency_pairs']}")
    except Exception:
        print("  (Conversion skipped - no network)")
    
    # Cleanup old records
    removed = manager.cleanup_cache()
    print(f"\nCleaned up {removed} old records")


def demo_error_handling():
    """Demo 6: Error handling with helpful messages"""
    print_section("6. Error Handling")
    
    config = CurrencyConfig(
        application_name="ErrorDemo",
        allowed_currencies=['USD', 'EGP']
    )
    
    manager = CurrencyManager(config)
    
    # Test 1: Invalid currency code
    print("Test 1: Invalid currency code")
    try:
        manager.create_money('100', 'USDD')  # Typo
    except Exception as e:
        print(f"  Error: {e}")
    
    # Test 2: Currency not allowed
    print("\nTest 2: Currency not allowed")
    try:
        manager.create_money('100', 'EUR')
    except CurrencyNotAllowedError as e:
        print(f"  Error: {e}")
    
    # Test 3: Currency mismatch in operations
    print("\nTest 3: Currency mismatch in operations")
    try:
        money_usd = manager.create_money('100', 'USD')
        money_egp = manager.create_money('1000', 'EGP')
        manager.add(money_usd, money_egp)  # Different currencies
    except Exception as e:
        print(f"  Error: {e}")


def demo_safe_string_operations():
    """Demo 7: Safe string operations"""
    print_section("7. Safe String Operations (No Crashes!)")
    
    config = CurrencyConfig(application_name="SafeDemo")
    manager = CurrencyManager(config)
    
    money = manager.create_money('100.50', 'USD')
    
    # All these are safe!
    print(f"Using format(): {manager.format(money)}")
    print(f"In f-string: {manager.format(money, locale='en_US')}")
    print(f"With print: {manager.format(money, locale='fr_FR')}")
    
    # Create a list of money objects
    money_list = [
        manager.create_money('10', 'USD'),
        manager.create_money('20', 'USD'),
        manager.create_money('30', 'USD'),
    ]
    
    formatted_list = [manager.format(m) for m in money_list]
    print(f"List of money: {formatted_list}")


def demo_configuration_comparison():
    """Demo 8: Configuration comparison"""
    print_section("8. Configuration Comparison")
    
    # Permissive config
    print("Permissive Configuration:")
    config_permissive = CurrencyConfig(
        application_name="PermissiveApp",
        allow_cache_fallback=True,
        allowed_currencies=None
    )
    print(f"  Cache fallback: {config_permissive.allow_cache_fallback}")
    print(f"  Allowed currencies: {config_permissive.get_allowed_currencies_str()}")
    print(f"  Exchange strategy: {config_permissive.default_exchange_strategy}")
    
    # Strict config
    print("\nStrict Configuration:")
    config_strict = CurrencyConfig(
        application_name="StrictApp",
        allow_cache_fallback=False,
        allowed_currencies=['USD', 'EGP'],
        default_exchange_strategy='live',
        cache_max_records=10,
        cache_retention_days=7
    )
    print(f"  Cache fallback: {config_strict.allow_cache_fallback}")
    print(f"  Allowed currencies: {config_strict.get_allowed_currencies_str()}")
    print(f"  Exchange strategy: {config_strict.default_exchange_strategy}")
    print(f"  Max cache records: {config_strict.cache_max_records}")
    print(f"  Cache retention: {config_strict.cache_retention_days} days")


def main():
    """Run all demonstrations"""
    print("\n" + "=" * 70)
    print(" ROBUST CURRENCY CONVERSION SOLUTION - DEMONSTRATION")
    print("=" * 70)
    
    try:
        demo_basic_usage()
        demo_fuzzy_locale_matching()
        demo_strict_configuration()
        demo_currency_conversion()
        demo_cache_management()
        demo_error_handling()
        demo_safe_string_operations()
        demo_configuration_comparison()
        
        print("\n" + "=" * 70)
        print(" ✓ All demonstrations completed successfully!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n\n✗ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
