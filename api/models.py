from dataclasses import dataclass, field
from typing import Any, Dict, Iterable


@dataclass
class FizzBuzzSequence:
    """Data class for FizzBuzz sequence data."""

    data: Iterable
    fizz: int = field(init=False)
    buzz: int = field(init=False)
    fizzbuzz: int = field(init=False)
    digits: int = field(init=False)

    def __len__(self) -> int:
        return len(self.data)

    def __post_init__(self):
        self.fizz = self.data.count("Fizz")
        self.buzz = self.data.count("Buzz")
        self.fizzbuzz = self.data.count("FizzBuzz")
        self.digits = len(self.data) - (self.fizz + self.buzz + self.fizzbuzz)

    def get_data_summary(self) -> Dict[str, Any]:
        """Output a dictionary of the sequence data.

        Returns:
            Dict[str, Any]: JSON data
        """
        return {
            "count": len(self),
            "fizz": self.fizz,
            "buzz": self.buzz,
            "fizzbuzz": self.fizzbuzz,
            "digits": self.digits,
            "sequence": self.data,
        }
