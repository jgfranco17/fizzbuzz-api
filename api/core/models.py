from typing import List

from pydantic import BaseModel, EmailStr


class FizzBuzzSequence(BaseModel):
    """Data class for FizzBuzz sequence data."""

    fizz: int
    buzz: int
    fizzbuzz: int
    digits: int
    sequence: List[str]

    def __len__(self) -> int:
        return len(self.sequence)

    @classmethod
    def from_sequence(cls, data: List[str]) -> "FizzBuzzSequence":
        """Convert a sequence into a FizzBuzzSequence model.

        Args:
            data (List[str]): Raw sequence data

        Returns:
            FizzBuzzSequence: Data model
        """
        fizz = data.count("Fizz")
        buzz = data.count("Buzz")
        fizzbuzz = data.count("FizzBuzz")
        digits = len(data) - (fizz + buzz + fizzbuzz)
        return cls(
            fizz=fizz,
            buzz=buzz,
            fizzbuzz=fizzbuzz,
            digits=digits,
            sequence=data,
        )


class ProjectAuthor(BaseModel):
    name: str
    github_username: str
    email: EmailStr


class HealthCheck(BaseModel):
    status: str
