"""
Demo of pypenny's unified API

Shows the simple, intuitive interface for currency operations.
"""

import pypenny as pp


def main():
    print("=" * 70)
    print(" pypenny - Unified API Demo")
    print("=" * 70)
    
    # Configure once
    print("\n1. Configuration")
    pp.config(
        application_name="UnifiedAPIDemo",
        allowed_currencies=['USD', 'EGP', 'EUR'],
        allow_cache_fallback=True
    )
    print("✓ Configured pypenny")
    
    # Create money using the Money class
    print("\n2. Creating Money")
    money_usd = pp.Money('100', 'USD')
    money_egp = pp.Money('1500', 'EGP')
    print(f"Created: {money_usd}")
    print(f"Created: {money_egp}")
    
    # Arithmetic with dunder methods
    print("\n3. Arithmetic Operations (Dunder Methods)")
    money1 = pp.Money('50', 'USD')
    money2 = pp.Money('30', 'USD')
    
    print(f"money1 = {money1}")
    print(f"money2 = {money2}")
    print(f"money1 + money2 = {money1 + money2}")
    print(f"money1 - money2 = {money1 - money2}")
    print(f"money1 * 2 = {money1 * 2}")
    print(f"money1 / 2 = {money1 / 2}")
    print(f"money1 // 3 = {money1 // 3}")
    print(f"money1 ** 2 = {money1 ** 2}")
    
    # Functional style arithmetic
    print("\n4. Arithmetic Operations (Functional Style)")
    result_add = pp.add(money1, money2)
    result_sub = pp.subtract(money1, money2)
    result_mul = pp.multiply(money1, 2)
    result_div = pp.divide(money1, 2)
    
    print(f"pp.add(money1, money2) = {result_add}")
    print(f"pp.subtract(money1, money2) = {result_sub}")
    print(f"pp.multiply(money1, 2) = {result_mul}")
    print(f"pp.divide(money1, 2) = {result_div}")
    
    # Comparison operations
    print("\n5. Comparison Operations")
    print(f"money1 > money2: {money1 > money2}")
    print(f"money1 < money2: {money1 < money2}")
    print(f"money1 == money2: {money1 == money2}")
    print(f"money1 >= money2: {money1 >= money2}")
    
    # Formatting
    print("\n6. Formatting")
    money = pp.Money('100.50', 'USD')
    print(f"en_US: {pp.format(money, locale='en_US')}")
    print(f"fr_FR: {pp.format(money, locale='fr_FR')}")
    print(f"de_DE: {pp.format(money, locale='de_DE')}")
    
    # Currency conversion
    print("\n7. Currency Conversion")
    try:
        usd_money = pp.Money('100', 'USD')
        print(f"Original: {pp.format(usd_money, locale='en_US')}")
        
        egp_money = pp.convert(usd_money, 'EGP')
        print(f"Converted to EGP: {pp.format(egp_money, locale='ar_EG')}")
        
        eur_money = pp.convert(usd_money, 'EUR')
        print(f"Converted to EUR: {pp.format(eur_money, locale='de_DE')}")
    except Exception as e:
        print(f"Conversion error: {e}")
        print("(This is expected if no network connection)")
    
    # Sum with built-in sum()
    print("\n8. Using sum() with Money")
    items = [
        pp.Money('10', 'USD'),
        pp.Money('20', 'USD'),
        pp.Money('30', 'USD'),
    ]
    total = sum(items, pp.Money.zero('USD'))
    print(f"Items: {[str(m) for m in items]}")
    print(f"Total: {total}")
    
    # Cache management
    print("\n9. Cache Management")
    stats = pp.get_cache_stats()
    print(f"Cache stats: {stats}")
    
    print("\n" + "=" * 70)
    print(" ✓ Unified API Demo Complete!")
    print("=" * 70)
    print("\nKey Features:")
    print("  • Simple import: import pypenny as pp")
    print("  • Intuitive Money class with dunder methods")
    print("  • Functional API for all operations")
    print("  • One-time configuration")
    print("  • Works with Python's built-in functions (sum, abs, etc.)")


if __name__ == "__main__":
    main()
