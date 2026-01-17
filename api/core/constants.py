from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class EnvironmentVariables:
    REDIS_HOST: Final[str] = "REDIS_HOST"


@dataclass(frozen=True)
class RedisConfigs:
    LOCAL: Final[str] = "localhost"
    DEFAULT_HOST: Final[str] = "redis-cache"
    DEFAULT_PORT: Final[int] = 6379


@dataclass(frozen=True)
class SequenceWords:
    Fizz: Final[str] = "Fizz"
    Buzz: Final[str] = "Buzz"
    FizzBuzz: Final[str] = "FizzBuzz"
