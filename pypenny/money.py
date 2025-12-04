"""
Money wrapper class with dunder methods for arithmetic operations
"""

from decimal import Decimal
from typing import Union, Optional
from moneyed import Money as MoneyedMoney

from .exceptions import CurrencyMismatchError


class Money:
    """
    Wrapper around py-moneyed Money with enhanced arithmetic operations.
    
    Provides dunder methods for intuitive arithmetic while maintaining
    currency safety and proper error handling.
    
    Example:
        >>> money1 = Money('100', 'USD')
        >>> money2 = Money('50', 'USD')
        >>> total = money1 + money2  # $150
        >>> doubled = money1 * 2     # $200
    """
    
    def __init__(
        self,
        amount: Union[str, Decimal, int, float],
        currency_code: str
    ):
        """
        Initialize Money object.
        
        Args:
            amount: Amount (string, Decimal, int, or float)
            currency_code: Currency code (e.g., 'USD', 'EGP')
        """
        if not isinstance(amount, Decimal):
            amount = Decimal(str(amount))
        
        self._money = MoneyedMoney(amount, currency_code)
    
    @property
    def amount(self) -> Decimal:
        """Get the amount as Decimal"""
        return self._money.amount
    
    @property
    def currency(self):
        """Get the currency object"""
        return self._money.currency
    
    @property
    def currency_code(self) -> str:
        """Get the currency code"""
        return self._money.currency.code
    
    def get_moneyed_object(self) -> MoneyedMoney:
        """Get the underlying py-moneyed Money object"""
        return self._money
    
    # Arithmetic dunder methods
    
    def __add__(self, other: 'Money') -> 'Money':
        """Add two Money objects (money1 + money2)"""
        if not isinstance(other, Money):
            raise TypeError(f"Cannot add Money with {type(other).__name__}")
        
        if self.currency != other.currency:
            raise CurrencyMismatchError(
                "addition",
                self.currency_code,
                other.currency_code
            )
        
        result = self._money + other._money
        return Money._from_moneyed(result)
    
    def __radd__(self, other):
        """Right-hand addition (other + money)"""
        if other == 0:  # Support sum() function
            return self
        return self.__add__(other)
    
    def __sub__(self, other: 'Money') -> 'Money':
        """Subtract two Money objects (money1 - money2)"""
        if not isinstance(other, Money):
            raise TypeError(f"Cannot subtract {type(other).__name__} from Money")
        
        if self.currency != other.currency:
            raise CurrencyMismatchError(
                "subtraction",
                self.currency_code,
                other.currency_code
            )
        
        result = self._money - other._money
        return Money._from_moneyed(result)
    
    def __mul__(self, other: Union[int, float, Decimal]) -> 'Money':
        """Multiply Money by scalar (money * 2)"""
        if not isinstance(other, (int, float, Decimal)):
            raise TypeError(f"Cannot multiply Money by {type(other).__name__}")
        
        result = self._money * other
        return Money._from_moneyed(result)
    
    def __rmul__(self, other: Union[int, float, Decimal]) -> 'Money':
        """Right-hand multiplication (2 * money)"""
        return self.__mul__(other)
    
    def __truediv__(self, other: Union[int, float, Decimal]) -> 'Money':
        """Divide Money by scalar (money / 2)"""
        if not isinstance(other, (int, float, Decimal)):
            raise TypeError(f"Cannot divide Money by {type(other).__name__}")
        
        if other == 0:
            raise ZeroDivisionError("Cannot divide money by zero")
        
        result = self._money / other
        return Money._from_moneyed(result)
    
    def __floordiv__(self, other: Union[int, float, Decimal]) -> 'Money':
        """Floor divide Money by scalar (money // 2)"""
        if not isinstance(other, (int, float, Decimal)):
            raise TypeError(f"Cannot floor divide Money by {type(other).__name__}")
        
        if other == 0:
            raise ZeroDivisionError("Cannot divide money by zero")
        
        # py-moneyed doesn't support //, so we implement it manually
        result_amount = self.amount // Decimal(str(other))
        return Money(result_amount, self.currency_code)
    
    def __pow__(self, exponent: Union[int, float, Decimal]) -> 'Money':
        """Raise Money amount to power (money ** 2)"""
        result_amount = self.amount ** Decimal(str(exponent))
        return Money(result_amount, self.currency_code)
    
    # Comparison dunder methods
    
    def __eq__(self, other) -> bool:
        """Check equality (money1 == money2)"""
        if not isinstance(other, Money):
            return False
        return self._money == other._money
    
    def __ne__(self, other) -> bool:
        """Check inequality (money1 != money2)"""
        return not self.__eq__(other)
    
    def __lt__(self, other: 'Money') -> bool:
        """Less than comparison (money1 < money2)"""
        if not isinstance(other, Money):
            raise TypeError(f"Cannot compare Money with {type(other).__name__}")
        
        if self.currency != other.currency:
            raise CurrencyMismatchError(
                "comparison",
                self.currency_code,
                other.currency_code
            )
        
        return self._money < other._money
    
    def __le__(self, other: 'Money') -> bool:
        """Less than or equal (money1 <= money2)"""
        return self.__lt__(other) or self.__eq__(other)
    
    def __gt__(self, other: 'Money') -> bool:
        """Greater than comparison (money1 > money2)"""
        if not isinstance(other, Money):
            raise TypeError(f"Cannot compare Money with {type(other).__name__}")
        
        if self.currency != other.currency:
            raise CurrencyMismatchError(
                "comparison",
                self.currency_code,
                other.currency_code
            )
        
        return self._money > other._money
    
    def __ge__(self, other: 'Money') -> bool:
        """Greater than or equal (money1 >= money2)"""
        return self.__gt__(other) or self.__eq__(other)
    
    # Unary operations
    
    def __neg__(self) -> 'Money':
        """Negate Money (-money)"""
        result = -self._money
        return Money._from_moneyed(result)
    
    def __pos__(self) -> 'Money':
        """Positive Money (+money)"""
        return self
    
    def __abs__(self) -> 'Money':
        """Absolute value (abs(money))"""
        result = abs(self._money)
        return Money._from_moneyed(result)
    
    # String representation
    
    def __repr__(self) -> str:
        """Developer-friendly representation"""
        return f"Money('{self.amount}', '{self.currency_code}')"
    
    def __str__(self) -> str:
        """User-friendly string (use format() for locale-aware)"""
        return f"{self.currency_code} {self.amount}"
    
    # Helper methods
    
    @classmethod
    def _from_moneyed(cls, moneyed_obj: MoneyedMoney) -> 'Money':
        """Create Money from py-moneyed Money object"""
        instance = cls.__new__(cls)
        instance._money = moneyed_obj
        return instance
    
    @classmethod
    def zero(cls, currency_code: str) -> 'Money':
        """Create zero money in given currency"""
        return cls('0', currency_code)
