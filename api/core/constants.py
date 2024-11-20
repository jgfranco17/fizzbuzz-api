from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class EnvironmentVariables:
    REDIS_HOST: Final[str] = "REDIS_HOST"


@dataclass(frozen=True)
class RedisConfigs:
    LOCAL: Final[str] = "localhost"
    DEFAULT_PORT: Final[int] = 6379
