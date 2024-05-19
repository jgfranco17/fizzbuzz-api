from typing import Any, Dict, List

from pydantic import BaseModel, EmailStr


class FizzBuzzSequence(BaseModel):
    """Data class for FizzBuzz sequence data."""

    fizz: int
    buzz: int
    fizzbuzz: int
    digits: int
    sequence: List[str]

    def __len__(self) -> int:
        return len(self.data)


def create_model_from_sequence(data: List[str]) -> FizzBuzzSequence:
    fizz = data.count("Fizz")
    buzz = data.count("Buzz")
    fizzbuzz = data.count("FizzBuzz")
    digits = len(data) - (fizz + buzz + fizzbuzz)
    return FizzBuzzSequence(
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


class ServiceInfo(BaseModel):
    project_name: str
    description: str
    repository_url: str
    license: str
    version: str
    language: List[str]
    frameworks: List[str]
    authors: List[ProjectAuthor]
    last_updated_on: str


class HealthCheck(BaseModel):
    status: str
